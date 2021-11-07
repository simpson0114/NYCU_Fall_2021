TARGET := pi.out
CPP := pi.c

CXX := gcc

CFLAGS := -std=gnu99 -Ofast
CFLAGS += -ffast-math -mavx -mavx2 -mfma -finline-functions

THREAD := -pthread

all: $(CPP)
	$(CXX) $(CPP) -o $(TARGET) $(CFLAGS) $(THREAD)

clean:
	rm *.out *.o