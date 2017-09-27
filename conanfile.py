from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment,tools
from os import chdir
from glob import glob

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
        src_dir = "{staging_dir}/src/fuse-{v}".format(staging_dir=self.staging_dir, v=self.version)
        if self.settings.os == "Android":
            for file in sorted(glob("patch/*.patch")):
                self.output.info("Applying patch '{file}'".format(file=file))
                tools.patch(base_path=src_dir, patch_file=file, strip=0)

        shared_definition = "--enable-static", "--disable-shared"
        if self.options["libfuse"].shared:
            shared_definition = "--enable-shared", "--disable-static"
        chdir("{staging_dir}/src/fuse-{v}".format(staging_dir=self.staging_dir, v=self.version))
        env_build = AutoToolsBuildEnvironment(self)
        env_build.configure(args=["--prefix={staging_dir}".format(staging_dir=self.staging_dir),
            shared_definition[0], shared_definition[1], "--disable-util", "--disable-example", "--verbose"])
        env_build.make(['V=1', 'install'])

    def do_package_info(self):
        self.cpp_info.libs = ["fuse"]
