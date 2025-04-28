LIBDIR="$(find /usr/lib -maxdepth 1 -type d -name '*-linux-*' | grep -v '/config-' | head -n1)";
ln -sf "${LIBDIR}/libglut.so.3.12" "${LIBDIR}/libglut.so.3";
