#include "mock_hw.h"
#include "../../bleuart/inc/app_keyscan.h"
int main(void){unsigned i,j;uint32_t raw[2]={0u,0x04000000u};
 assert(KEYSCAN_KEY18==18 && KEYSCAN_KEY_MAX==19);
 assert(sizeof(keyscan_map)/sizeof(keyscan_map[0])==KEYSCAN_KEY_MAX+1);
 assert(keyscan_map[18][0]==0&&keyscan_map[18][1]==0x04000000u);
 assert(keyscan_is_key_pressed(raw,18));
 for(i=1;i<KEYSCAN_KEY_MAX;i++){
  if(i!=18)assert(!keyscan_is_key_pressed(raw,(uint8_t)i));
  for(j=i+1;j<KEYSCAN_KEY_MAX;j++)assert(memcmp(keyscan_map[i],keyscan_map[j],sizeof(keyscan_map[i]))!=0);
 }
 puts("matrix: actual 18-key table, PB9--PA6 bit26, unique original keys, new key isolation PASS");return 0;}
