#define FUSE_USE_VERSION 26
#include <fuse.h>
#include <cstring>

int
main(int argc, char* argv[])
{
	fuse_operations op;
	memset(&op, 0, sizeof(op));
	char name[] = {'l', 'i', 'b', 'f', 'u', 's', 'e', '\0'};
	char minus_f[] = {'-', 'f', '\0'};
	char mpoint[] = { '/', 't', 'm', 'p', '\0'};
	char* fuse_argv[4] = { name, minus_f, mpoint, nullptr };
	int fuse_argc = 3;
	int mt = 0;
	char* mountpoint  = nullptr;
	fuse* fuse = fuse_setup(fuse_argc, fuse_argv, &op, sizeof(op),
			&mountpoint, &mt, nullptr);
	if (fuse == nullptr)
		return 0;
	fuse_teardown(fuse, mpoint);
	return 0;
}

