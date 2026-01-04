#!/bin/sh

mntroot rw

mkdir -p /mnt/us/inkframe
cp /mnt/us/inkframe_install/inkframe.sh /mnt/us/inkframe/inkframe.sh
chmod +x /mnt/us/inkframe/inkframe.sh

cat << 'EOF' > /etc/init.d/inkframe
#!/bin/sh
/mnt/us/inkframe/inkframe.sh &
EOF

chmod +x /etc/init.d/inkframe
ln -s /etc/init.d/inkframe /etc/rc5.d/S99inkframe

mntroot ro
