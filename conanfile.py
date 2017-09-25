from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment,tools
from os import chdir


class LibFuseConan(NxConanFile):
    name = "libfuse"
    version = "2.9.7"
    license = "GPLv2"
    url = "https://github.com/hoxnox/conan-libfuse"
    license = "https://github.com/libfuse/libfuse/blob/master/COPYING"
    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"
    description = "he reference implementation of the Linux FUSE (Filesystem in Userspace) interface"
    options = {"shared":[True, False]}
    default_options = "shared=False"

    def do_source(self):
        self.retrieve("832432d1ad4f833c20e13b57cf40ce5277a9d33e483205fc63c78111b3358874",
                [
                    "vendor://libfuse/libfuse/libfuse-{v}.tar.gz".format(v=self.version),
                    "https://github.com/libfuse/libfuse/releases/download/fuse-{v}/fuse-{v}.tar.gz".format(v=self.version)
                ],
                "libfuse-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        tools.untargz("libfuse-{v}.tar.gz".format(v=self.version), "{staging_dir}/src".format(staging_dir=self.staging_dir))
        shared_definition = "--enable-static --disable-shared"
        if self.options.shared:
            shared_definition = "--enable-shared --disable-static"
        chdir("{staging_dir}/src/fuse-{v}".format(staging_dir=self.staging_dir, v=self.version))
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("./configure prefix=\"{staging_dir}\" {shared} --disable-util --disable-example".format(
                staging_dir=self.staging_dir, shared=shared_definition))
            self.run("make install")

    def do_package_info(self):
        self.cpp_info.libs = ["fuse"]
