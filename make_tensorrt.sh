echo "make clean ..."
make clean -c /root/tensorrt_demos/plugins
echo "make ..."
make -c /root/tensorrt_demos/plugins
echo "copy to /app/plugins"
cp -r /root/tensorrt_demos/plugins /app/plugins
