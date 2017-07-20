CFLAGS+=-std=c11
CFLAGS+=-Wall -Wextra -Wpedantic

LDLIBS+=-lm -lssl -lcrypto

TARGETS=sludger chlorinator

all: $(TARGETS)

chlorinator: chlorinator.o structs.o networking.o crypto_scrypt-nosse.o sha256.o

sludger: sludger.o structs.o networking.o crypto_scrypt-nosse.o sha256.o

clean:
	$(RM) *.o $(TARGETS)

.phony: all clean
