#include <stdio.h>
#include <stdlib.h>
#include <math.h>

enum cache_block_state {
	INVALID,
	VALID
};

typedef unsigned uint;

typedef struct cache_block{
	enum cache_block_state status;
	uint tag;
	uint time;
}cache_block;

uint sets;
uint assoc;
uint block;
uint block_log2 = 0;
uint total_cache_accesses = 0;
uint total_cache_misses = 0;
uint sim_time = 0;
struct cache_block *cache;

void cache_access(char inst_type, uint addr);

void cache_access(char inst_type, uint addr){
    uint temp = sets;
    uint sets_log2 = 0;
    while (temp >>= 1) ++sets_log2;
    uint block_n = addr>>block_log2;
    uint loc = (block_n%sets)*assoc;
    uint tag = addr>>(sets_log2+block_log2);
    for(int i = 0; i<assoc; i++){
        if(cache[loc+i].status==VALID&&cache[loc+i].tag == tag){
            cache[loc+i].time = sim_time;
            return;
        }
    }
    total_cache_misses++;
    for(int i = 0; i<assoc; i++){
        if(cache[loc+i].status==INVALID){
            cache[loc+i].time = sim_time;
            cache[loc+i].tag = tag;
            cache[loc+i].status = VALID;
            return;
        }
    }
    int minTime = cache[loc].time;
    int minTimeIndex = loc;   
    for(int i = 0; i<assoc; i++){
        if(cache[loc+i].time<minTime){
            minTimeIndex = loc+i;
            minTime = cache[loc+i].time;
        }
    }
    cache[minTimeIndex].time = sim_time;
    cache[minTimeIndex].tag = tag;      
}

int main(int argc, char** argv)
{
    if (argc != 5) {
        printf("Usage: %s <number_of_sets> <associativity> <cache_block_size> <trace_file>\n", argv[0]);
        return -1;
    }
    /*
       input parameters
       argv[1] = number of sets
       argv[2] = associativity
       argv[3] = cache block size
       argv[4] = trace file name
    */
    char inst_type = 0;
    uint addr = 0;
    sets = atoi(argv[1]);
    assoc = atoi(argv[2]);
    block = atoi(argv[3]);
    while (block >>= 1) ++block_log2;
    FILE *fp = fopen(argv[4], "r");
    if (fp == NULL){
        printf("trace file does not exist\n");
        return -1;  
    }

    cache=malloc(sizeof(struct cache_block)*sets*assoc);
    int i=0;
    for(i=0;i<sets*assoc;i++){
        cache[i].time=0;
        cache[i].tag=0;
        cache[i].status=INVALID;
    }

    while (fscanf(fp, "%c 0x%x\n", &inst_type, &addr) != EOF) {
        cache_access(inst_type, addr);
        total_cache_accesses++;
	    sim_time++;
    }

    printf("Cache accesses = %u\n", total_cache_accesses);
    printf("Cache misses = %u\n", total_cache_misses);
    printf("Miss rate = %.3f\n", (float)(total_cache_misses)/(float)(total_cache_accesses));
    free(cache);
    fclose(fp);

    return 0;
}

//void cache_access(char inst_type, uint addr)
//{
//    printf("type = %c, addr = 0x%08x\n", inst_type, addr); 
//}

