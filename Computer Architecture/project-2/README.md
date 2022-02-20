# How to build
```bash
make
```

# How to run

```bash
./cache_sim <nsets> <assoc> <block_size> <trace_file_name>
```
# Sample tests

- Test 1

```bash
./cache_sim 32 2 32 test.trace
```

- Expected output

```bash
Cache accesses = 10
Cache misss = 7
```
- Test 2

```bash
./cache_sim 32 2 32 ls.trace
```
- Expected output

```bash
Cache accesses = 382691
Cache misss = 27108
```


