import json
import journal
import utils.disk_utils as utils
import utils.checks as checks
from syscommands import cmd, chroot

with open("config.json", "r") as config:
    config = json.load(config)

diskpath = utils.get_disk_info(config["disk"])
p1 = utils.get_disk_info(config["disk"], "1") 
p2 = utils.get_disk_info(config["disk"], "2") 
partsize = "32GB"
try:
    if config["reducedpartsize"]:
        partsize = "8GB"
except:
    None

checks.run_checks()

pacstrap_packages = "base linux linux-firmware base-devel amd-ucode nano networkmanager grub efibootmgr git lvm2 cryptsetup thin-provisioning-tools"
mkinitcpio_hooks = "base systemd autodetect microcode modconf kms keyboard sd-vconsole block sd-encrypt lvm2 filesystems fsck"

def preinstall():
    journal.section("Preparing disk")
    cmd(f'dd if=/dev/zero of={diskpath} bs=1M count=10')
    cmd(f'wipefs -af {diskpath}')
    cmd(f'sgdisk -Z {diskpath}')
    cmd(f'udevadm settle')
    journal.success()

preinstall()

def partition():
    journal.section("Partitioning")
    cmd(f'parted {diskpath} --script mklabel gpt '
        f'mkpart primary fat32 1MiB 513MiB '
        f'set 1 esp on '
        f'mkpart primary 513MiB 100%')
    cmd(f'partprobe {diskpath}')
    cmd(f'udevadm settle')
    cmd(f'mkfs.fat -F32 {p1}')
    journal.success()

partition()

def encrypt():
    journal.section("Encrypting")
    cmd(f'echo -n {config["encryption_password"]} | cryptsetup luksFormat {p2} --key-file -')
    cmd(f'echo -n {config["encryption_password"]} | cryptsetup open {p2} cryptlvm --key-file -')
    journal.success()

encrypt()

def setuplvm():
    journal.section("Setting up LVM")
    volgroup = "/dev/SystemVolumeGroup"
    root = volgroup + "/root"
    home = volgroup + "/home"
    swap = volgroup + "/swap"
    cmd('pvcreate /dev/mapper/cryptlvm')
    cmd('vgcreate SystemVolumeGroup /dev/mapper/cryptlvm')
    cmd('lvcreate -L 4GB -n swap SystemVolumeGroup')
    cmd(f'lvcreate -L {partsize} -n root SystemVolumeGroup')
    cmd('lvcreate -l 100%FREE -n home SystemVolumeGroup')
    journal.section("Formatting logical volumes")
    cmd(f'mkfs.ext4 {root}')
    cmd(f'mkfs.ext4 {home}')
    cmd(f'mkswap {swap}')
    journal.section("Mounting filesystems")
    cmd(f'mount {root} /mnt')
    cmd(f'mount --mkdir {home} /mnt/home')
    cmd(f'swapon {swap}')
    cmd(f'mount --mkdir {p1} /mnt/efi')
    journal.success()

setuplvm()

def base_system():
    journal.section("Installing base system. This may take a while.")
    cmd(f'pacstrap -K /mnt {pacstrap_packages}')
    cmd("genfstab -U /mnt >> /mnt/etc/fstab")
    journal.success()

base_system()

def localization():
    journal.section("Configuring locale")
    chroot('ln -sf /usr/share/zoneinfo/Portugal /etc/localtime')
    chroot('hwclock --systohc')
    chroot('echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen')
    chroot('touch /etc/vconsole.conf')
    chroot('echo "KEYMAP=de-latin1" >> /etc/vconsole.conf')
    chroot('locale-gen')
    chroot('echo "LANG=en_US.UTF-8" > /etc/locale.conf')
    chroot('echo "archlinux" > /etc/hostname')
    journal.success()

localization()

def mkinitcpio():
    journal.section("Configuring mkinitcpio")
    chroot("pacman -Q lvm2")
    chroot(f'sed -i "s/^HOOKS=.*/HOOKS=({mkinitcpio_hooks})/" /etc/mkinitcpio.conf')
    chroot('mkinitcpio -P')
    journal.success()

mkinitcpio()

def bootloader():
    journal.section("Configuring bootloader")
    uuid = utils.get_uuid(p2)
    journal.info(f'UUID: {uuid}') # DEBUG LINE
    chroot('sed -i "s/^.*GRUB_ENABLE_CRYPTODISK.*/GRUB_ENABLE_CRYPTODISK=y/" /etc/default/grub')
    chroot(f'sed -i "s/^GRUB_CMDLINE_LINUX=.*/GRUB_CMDLINE_LINUX=\\"rd.luks.uuid={uuid}\\"/" /etc/default/grub')
    chroot('grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB')
    chroot('grub-mkconfig -o /boot/grub/grub.cfg')
    chroot('grep ^HOOKS /etc/mkinitcpio.conf')
    journal.success()

bootloader()

def users():
    journal.section("Setting passwords and creating users")
    chroot(f'echo -n "root:{config["root_password"]}" | chpasswd')
    chroot(f'useradd -m -G wheel -s /bin/bash {config["user_name"]}')
    chroot(f'bash -c \'echo -n "{config["user_name"]}:{config["user_password"]}" | chpasswd\'')
    chroot('sed -i "s/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/" /etc/sudoers')
    journal.success()
users()

def finish():
    journal.section("Finishing")
    chroot('systemctl enable NetworkManager')
finish()

