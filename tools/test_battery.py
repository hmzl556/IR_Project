"""Exercise actual battery conversion/cache code with mocked ADC hardware."""
from pathlib import Path
import subprocess
import tempfile
r = Path(__file__).resolve().parents[1]
s = (r / "bleuart/src/bat_adc.c").read_text(encoding="utf-8")
constants = s[s.index("#define BAT_DIV_NUM"):s.index("/**")]
functions = s[s.index("static uint8_t bat_mv_to_percent"):]
mock = r'''#include <stdint.h>
#include <assert.h>
#include <stdio.h>
static unsigned lte, prepared, released, reads, fail;
static uint8_t g_audio_pcm_enabled;
#define LTE_EN_IS_ON() (lte)
#define ADC_CTRL_CH_5 5
#define co_printf(...) ((void)0)
static void bat_adc_hw_prepare(void){prepared++;}
static void bat_adc_hw_release(void){released++;}
static int bat_adc_read_once_raw(uint16_t *v){reads++;*v=700;return fail?-1:0;}
static uint32_t ADC_ConverValueToVoltage(uint16_t v,unsigned ch){(void)ch;return v;}
'''
main = r'''
int main(void){
 unsigned i; uint8_t valid;
 assert(bat_get_cached_level()==100);
 assert(bat_get_level_percent()==100 && reads==0 && prepared==0);
 lte=1; valid=bat_get_level_percent();
 assert(valid>0 && valid<100 && reads==8 && prepared==1 && released==1);
 lte=0;
 for(i=0;i<1000;i++) assert(bat_get_level_percent()==valid);
 assert(reads==8 && prepared==1 && bat_get_cached_level()==valid);
 assert(s_bat_level_cached==valid);
 lte=1;g_audio_pcm_enabled=1;
 assert(bat_get_level_percent()==valid && reads==8);
 g_audio_pcm_enabled=0;fail=1;
 assert(bat_get_level_percent()==valid && reads==16);
 lte=0;
 assert(bat_get_level_percent()==valid && bat_get_cached_level()==valid);
 puts("battery: initial 100%, valid ADC, 1000 LTE-off reads without ADC/cache reset, voice busy and ADC failure retention PASS");
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix="vcr_battery_") as d:
 p=Path(d); c=p/"battery.c"; exe=p/"battery.exe"
 c.write_text(mock+constants+functions+main,encoding="utf-8")
 subprocess.run(["gcc","-std=c99","-O2",str(c),"-o",str(exe)],check=True)
 subprocess.run([str(exe)],check=True)
