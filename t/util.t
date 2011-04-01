use strict;
use warnings;
use PlannedBlackoutJP::Util;
use Test::More;

ok is_galapagos({HTTP_USER_AGENT => 'DoCoMo/2.0 N901iS(c100;TB;W24H12)'});
ok is_galapagos({
    HTTP_USER_AGENT => 'KDDI-HI21 UP.Browser/6.0.2.254 (GUI) MMP/1.1'
});
ok is_galapagos({
    HTTP_USER_AGENT => 'SoftBank/1.0/910T/TJ001/SN123456789012345 Browser/' . 
                       'NetFront/3.3 Profile/MIDP-2.0 Configuration/CLDC-1.1'
});

ok ! is_galapagos({
    HTTP_USER_AGENT => 'Mozilla/4.0 ' . 
                       '(compatible; GoogleToolbar 5.0.2124.2070; ' .
                       'Windows 6.0; MSIE 8.0.6001.18241)'
});
ok ! is_galapagos({
    HTTP_USER_AGENT => 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_1 like ' . 
                       'Mac OS X; ja-jp) AppleWebKit/525.18.1 ' . 
                       '(KHTML, like Gecko) Version/3.1.1 ' . 
                       'Mobile/5F136 Safari/525.20'
});

done_testing;
