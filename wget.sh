#!/bin/bash
echo " -> Downloading paper jar"
wget -q --show-progress -O ./server.jar https://fill-data.papermc.io/v1/objects/da497e12b43e5b61c5df150e4bfd0de0f53043e57d2ac98dd59289ee9da4ad68/paper-1.21.11-127.jar
echo " -> Downloading plugin tarball..."
wget -q --show-progress -O ./plugins.tar.zst https://raw.githubusercontent.com/thedistromaker/transfer-repo/data/plugins.tar.zst
echo " -> Downloading Azul Zulu JDK 21..."
wget -q --show-progress -O ./zulu-jdk21.tar.gz https://cdn.azul.com/zulu/bin/zulu21.48.17-ca-jdk21.0.10-linux_x64.tar.gz
echo " -> Making MC directory..."
mkdir -p minecraft/bin minecraft/server
echo " -> Extracting Azul Zulu JDK 21..."
tar -xf ./zulu-jdk21.tar.gz -C minecraft/bin/
mv server.jar minecraft/server/
cd minecraft/bin
mv zulu21.48.17-ca-jdk21.0.10-linux_x64/* .
rm -rf zulu21.48.17-ca-jdk21.0.10-linux_x64
ln -s bin/java java
cd ../server/
echo " -> Setting up runfile..."
echo "#!/bin/bash" > run.sh
echo "" >> run.sh
echo "../bin/java -Xmx4G -Xms4G -jar -XX:+UseG1GC server.jar nogui" >> run.sh
echo " -> Starting for configuration..."
bash run.sh
sed s/false/true/ -i eula.txt
echo " -> Making runfile executable"
tar -xf ../../plugins.tar.zst -C ./plugins/
mv plugins/plugins/* plugins/
chmod +x run.sh
