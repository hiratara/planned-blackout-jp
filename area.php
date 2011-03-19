<code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br /></span><span style="color: #FF8000">/*&nbsp;<br />*&nbsp;停電時間検索PHP版<br />*<br />*&nbsp;@mnakajim&nbsp;の&nbsp;perl&nbsp;版を&nbsp;PHP&nbsp;に移植&nbsp;<br />*&nbsp;@author&nbsp;&nbsp;@_nat<br />*&nbsp;@version&nbsp;1.03<br />*<br />*&nbsp;DATA/all.all&nbsp;を読み込んで使います。<br />*&nbsp;<br />*&nbsp;INSTALL<br />*&nbsp;1.&nbsp;このスクリプト&nbsp;http://www.gosoudan.com/power/area.phps&nbsp;を<br />*&nbsp;&nbsp;&nbsp;&nbsp;ダウンロード、拡張子を.php&nbsp;に変更して配置する。<br />*&nbsp;2.&nbsp;http://www.gosoudan.com/power/DATA/all.all&nbsp;をダウンロードし、<br />*&nbsp;&nbsp;&nbsp;&nbsp;area.php&nbsp;をインストールしたフォルダの下にDATAフォルダを作り、<br />*&nbsp;&nbsp;&nbsp;&nbsp;その中に配置する。<br />*&nbsp;<br />*&nbsp;変更履歴<br />*&nbsp;2011-03-18&nbsp;iPhone&nbsp;対応<br />*&nbsp;2011-03-19&nbsp;輪番アルゴリズム化。これで原則プログラムアップデート必要なし。<br />*&nbsp;2011-03-19&nbsp;(1.03)&nbsp;group指定を可能に。<br />*&nbsp;<br />*&nbsp;TODO<br />*&nbsp;-&nbsp;関数にするとか,&nbsp;整理が必要。<br />*&nbsp;-&nbsp;Motd&nbsp;をマスターから取り寄せる形にしたい。<br />*/<br /></span><span style="color: #0000BB">$getcity</span><span style="color: #007700">=</span><span style="color: #0000BB">$_REQUEST</span><span style="color: #007700">[</span><span style="color: #DD0000">'city'</span><span style="color: #007700">];<br /></span><span style="color: #0000BB">$getcity</span><span style="color: #007700">=</span><span style="color: #0000BB">preg_replace</span><span style="color: #007700">(</span><span style="color: #DD0000">'/w+/'</span><span style="color: #007700">,</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #0000BB">$getcity</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">=</span><span style="color: #0000BB">$_REQUEST</span><span style="color: #007700">[</span><span style="color: #DD0000">'gid'</span><span style="color: #007700">];<br /></span><span style="color: #0000BB">$y</span><span style="color: #007700">=array(</span><span style="color: #DD0000">'日'</span><span style="color: #007700">,</span><span style="color: #DD0000">'月'</span><span style="color: #007700">,</span><span style="color: #DD0000">'火'</span><span style="color: #007700">,</span><span style="color: #DD0000">'水'</span><span style="color: #007700">,</span><span style="color: #DD0000">'木'</span><span style="color: #007700">,</span><span style="color: #DD0000">'金'</span><span style="color: #007700">,</span><span style="color: #DD0000">'土'</span><span style="color: #007700">);<br />if&nbsp;(</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">&gt;</span><span style="color: #0000BB">5&nbsp;</span><span style="color: #007700">||&nbsp;</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">&lt;=</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;<br />}<br /><br /><br /></span><span style="color: #0000BB">$s</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00,&nbsp;16:50-20:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">);<br /><br /></span><span style="color: #0000BB">$t0&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">time</span><span style="color: #007700">()&nbsp;+&nbsp;</span><span style="color: #0000BB">9</span><span style="color: #007700">*</span><span style="color: #0000BB">60</span><span style="color: #007700">*</span><span style="color: #0000BB">60</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$t1&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">$t0&nbsp;</span><span style="color: #007700">+&nbsp;</span><span style="color: #0000BB">86400</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$t2&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">$t1&nbsp;</span><span style="color: #007700">+&nbsp;</span><span style="color: #0000BB">86400</span><span style="color: #007700">;<br /><br /></span><span style="color: #0000BB">$bas&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'z'</span><span style="color: #007700">,</span><span style="color: #DD0000">'2011-03-18'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$os0&nbsp;</span><span style="color: #007700">=&nbsp;(</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'z'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t0</span><span style="color: #007700">)&nbsp;-&nbsp;</span><span style="color: #0000BB">$bas</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">+</span><span style="color: #0000BB">2&nbsp;</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$os1&nbsp;</span><span style="color: #007700">=&nbsp;(</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'z'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t1</span><span style="color: #007700">)&nbsp;-&nbsp;</span><span style="color: #0000BB">$bas</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">+</span><span style="color: #0000BB">2&nbsp;</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$os2&nbsp;</span><span style="color: #007700">=&nbsp;(</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'z'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t2</span><span style="color: #007700">)&nbsp;-&nbsp;</span><span style="color: #0000BB">$bas</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">+</span><span style="color: #0000BB">2&nbsp;</span><span style="color: #007700">;<br /><br /></span><span style="color: #FF8000">//&nbsp;Calculate&nbsp;Shift<br /></span><span style="color: #0000BB">$g&nbsp;</span><span style="color: #007700">=&nbsp;array(</span><span style="color: #0000BB">1</span><span style="color: #007700">,</span><span style="color: #0000BB">2</span><span style="color: #007700">,</span><span style="color: #0000BB">3</span><span style="color: #007700">,</span><span style="color: #0000BB">4</span><span style="color: #007700">,</span><span style="color: #0000BB">5</span><span style="color: #007700">);<br /><br />for(</span><span style="color: #0000BB">$i</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">&lt;</span><span style="color: #0000BB">5</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">++)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$g0</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=(</span><span style="color: #0000BB">$g</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]+</span><span style="color: #0000BB">$os0</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$g1</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=(</span><span style="color: #0000BB">$g</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]+</span><span style="color: #0000BB">$os1</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$g2</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=(</span><span style="color: #0000BB">$g</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]+</span><span style="color: #0000BB">$os2</span><span style="color: #007700">)%</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">$g0</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]==</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;</span><span style="color: #0000BB">$g0</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">$g1</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]==</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;</span><span style="color: #0000BB">$g1</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">$g2</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]==</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;</span><span style="color: #0000BB">$g2</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">]=</span><span style="color: #0000BB">5</span><span style="color: #007700">;<br />}<br /><br /><br /></span><span style="color: #0000BB">$td0&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'n/j'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t0</span><span style="color: #007700">)&nbsp;.&nbsp;</span><span style="color: #DD0000">"("&nbsp;</span><span style="color: #007700">.&nbsp;</span><span style="color: #0000BB">$y</span><span style="color: #007700">[</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'w'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t0</span><span style="color: #007700">)]&nbsp;.&nbsp;</span><span style="color: #DD0000">")"</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$td1&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'n/j'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t1</span><span style="color: #007700">)&nbsp;.&nbsp;</span><span style="color: #DD0000">"("&nbsp;</span><span style="color: #007700">.&nbsp;</span><span style="color: #0000BB">$y</span><span style="color: #007700">[</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'w'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t1</span><span style="color: #007700">)]&nbsp;.&nbsp;</span><span style="color: #DD0000">")"</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$td2&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'n/j'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t2</span><span style="color: #007700">)&nbsp;.&nbsp;</span><span style="color: #DD0000">"("&nbsp;</span><span style="color: #007700">.&nbsp;</span><span style="color: #0000BB">$y</span><span style="color: #007700">[</span><span style="color: #0000BB">date</span><span style="color: #007700">(</span><span style="color: #DD0000">'w'</span><span style="color: #007700">,</span><span style="color: #0000BB">$t2</span><span style="color: #007700">)]&nbsp;.&nbsp;</span><span style="color: #DD0000">")"</span><span style="color: #007700">;<br /><br /></span><span style="color: #0000BB">$file</span><span style="color: #007700">=</span><span style="color: #0000BB">file</span><span style="color: #007700">(</span><span style="color: #DD0000">"DATA/all.all"</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$count</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$nr</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">count</span><span style="color: #007700">(</span><span style="color: #0000BB">$file</span><span style="color: #007700">);<br />for(</span><span style="color: #0000BB">$i</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">&lt;</span><span style="color: #0000BB">$nr</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">++)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$line</span><span style="color: #007700">=</span><span style="color: #0000BB">$file</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$area&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">preg_split</span><span style="color: #007700">(</span><span style="color: #DD0000">'/\t/'</span><span style="color: #007700">,</span><span style="color: #0000BB">$line</span><span style="color: #007700">);<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$num&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">3</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">=</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">0</span><span style="color: #007700">].</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">1</span><span style="color: #007700">].</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">2</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">=</span><span style="color: #0000BB">preg_replace</span><span style="color: #007700">(</span><span style="color: #DD0000">'/&nbsp;/'</span><span style="color: #007700">,</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">);<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(</span><span style="color: #0000BB">$count&nbsp;</span><span style="color: #007700">%&nbsp;</span><span style="color: #0000BB">2&nbsp;</span><span style="color: #007700">==</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$bgcolor</span><span style="color: #007700">=</span><span style="color: #DD0000">'EEFFFF'</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$bgcolor</span><span style="color: #007700">=</span><span style="color: #DD0000">'FFEEFF'</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$num</span><span style="color: #007700">=</span><span style="color: #0000BB">intval</span><span style="color: #007700">(</span><span style="color: #0000BB">rtrim</span><span style="color: #007700">(</span><span style="color: #0000BB">$num</span><span style="color: #007700">));&nbsp;</span><span style="color: #FF8000">//&nbsp;Group&nbsp;number<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #007700">if&nbsp;(</span><span style="color: #0000BB">preg_match</span><span style="color: #007700">(</span><span style="color: #DD0000">"/$getcity/"</span><span style="color: #007700">,</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">))&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #FF8000">//&nbsp;echo&nbsp;$getcity&nbsp;.&nbsp;":"&nbsp;.&nbsp;$areaorg&nbsp;.":".&nbsp;$num&nbsp;.&nbsp;&nbsp;"&lt;br&gt;\n";<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$x0</span><span style="color: #007700">=</span><span style="color: #0000BB">$g0</span><span style="color: #007700">[</span><span style="color: #0000BB">$num</span><span style="color: #007700">-</span><span style="color: #0000BB">1</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$x1</span><span style="color: #007700">=</span><span style="color: #0000BB">$g1</span><span style="color: #007700">[</span><span style="color: #0000BB">$num</span><span style="color: #007700">-</span><span style="color: #0000BB">1</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$x2</span><span style="color: #007700">=</span><span style="color: #0000BB">$g2</span><span style="color: #007700">[</span><span style="color: #0000BB">$num</span><span style="color: #007700">-</span><span style="color: #0000BB">1</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">==</span><span style="color: #0000BB">0&nbsp;</span><span style="color: #007700">||&nbsp;</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">==</span><span style="color: #0000BB">$num</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">.=</span><span style="color: #DD0000">"&lt;tr&nbsp;bgcolor=$bgcolor&gt;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;td&gt;&lt;b&gt;$area[0]&nbsp;$area[1]&nbsp;$area[2]&lt;/b&gt;&lt;/td&gt;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;td&gt;$s[$x0]&lt;/td&gt;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;td&gt;$s[$x1]&lt;/td&gt;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;td&gt;$s[$x2]&lt;/td&gt;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;td&gt;第&nbsp;$num&nbsp;グループ&lt;/td&gt;&lt;/tr&gt;\n"</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$count</span><span style="color: #007700">++;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br />&nbsp;&nbsp;&nbsp;&nbsp;}<br />}<br /><br />if&nbsp;(!</span><span style="color: #0000BB">$count</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">=</span><span style="color: #DD0000">"&lt;tr&gt;&lt;td&nbsp;colspan=5&gt;計画停電のないエリアです。&lt;/td&gt;&lt;/tr&gt;"</span><span style="color: #007700">;<br />}<br />if&nbsp;(</span><span style="color: #0000BB">$count</span><span style="color: #007700">&gt;</span><span style="color: #0000BB">40</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">=</span><span style="color: #DD0000">"&lt;tr&gt;&lt;td&nbsp;colspan=5&gt;該当地域が多すぎです。詳細の地域名を入力してください。&lt;/td&gt;&lt;/tr&gt;"</span><span style="color: #007700">;<br />}<br /><br />function&nbsp;</span><span style="color: #0000BB">dd</span><span style="color: #007700">(</span><span style="color: #0000BB">$date</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$t1&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">strtotime</span><span style="color: #007700">(</span><span style="color: #DD0000">'2011-03-18'</span><span style="color: #007700">);<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$t2&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">strtotime</span><span style="color: #007700">(</span><span style="color: #0000BB">$date</span><span style="color: #007700">);<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$dd&nbsp;</span><span style="color: #007700">=&nbsp;(</span><span style="color: #0000BB">$t2&nbsp;</span><span style="color: #007700">-&nbsp;</span><span style="color: #0000BB">$t1</span><span style="color: #007700">)&nbsp;/&nbsp;(</span><span style="color: #0000BB">3600</span><span style="color: #007700">*</span><span style="color: #0000BB">24</span><span style="color: #007700">);<br />&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;</span><span style="color: #0000BB">$dd</span><span style="color: #007700">;<br /><br />}<br /></span><span style="color: #0000BB">header</span><span style="color: #007700">(</span><span style="color: #DD0000">"Content-type:&nbsp;text/html;charset=utf-8"</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">?&gt;<br /></span>&lt;html&gt;<br />&lt;head&gt;<br />&lt;title&gt;検索結果&lt;/title&gt;<br />&lt;meta&nbsp;name="viewport"&nbsp;content="width=device-width,&nbsp;initial-scale=1,&nbsp;maximum-scal<br />e=1"&gt;<br />&lt;/head&gt;<br />&lt;body&gt;<br />&lt;h1&nbsp;style="background-color:#ffdddd;border-left:15px&nbsp;#FFAAAA&nbsp;solid;"&gt;<br />停電時間検索結果&lt;/h1&gt;<br />&lt;h2&nbsp;style="border:1px&nbsp;#ff0000&nbsp;dashed;background-color:#ffddff;"&gt;<br />3/19-3/21の停電はなくなりました<br />。以下は、予定されていた停電です。<br />&lt;/h2&gt;<br /><span style="color: #0000BB">&lt;?=$count?&gt;</span>件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。&lt;BR&gt;<br />1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<br />&lt;table&nbsp;border=1&gt;&lt;tr&nbsp;bgcolor=#C0C0C0&gt;&lt;th&gt;地域&lt;/th&gt;&lt;th&gt;<span style="color: #0000BB">&lt;?=$td0?&gt;</span>&lt;/th&gt;&lt;th&gt;<span style="color: #0000BB">&lt;?=$td1?&gt;</span>&lt;/th&gt;&lt;th&gt;<span style="color: #0000BB">&lt;?=$td2?&gt;</span>&lt;/th&gt;&lt;th&gt;グループ&lt;/th&gt;&lt;/tr&gt;<br /><span style="color: #0000BB">&lt;?=$buf?&gt;<br /></span>&lt;/table&gt;&lt;a&nbsp;href=./index.html&gt;戻る&lt;/a&gt;<br /><br /><span style="color: #0000BB">&lt;?php<br /></span><span style="color: #FF8000">/*<br />echo&nbsp;"getgroup:".&nbsp;$getgroup;<br />echo&nbsp;"OS:&nbsp;$os0,&nbsp;$os1,&nbsp;$os2";<br />echo&nbsp;"&lt;br&nbsp;/&gt;g0:&nbsp;";<br />print_r($g0);<br />echo&nbsp;"\n&lt;br&nbsp;/&gt;g1:&nbsp;";<br />print_r($g1);<br />echo&nbsp;"\n&lt;br&nbsp;/&gt;g2:&nbsp;";<br />print_r($g2);<br />*/<br /></span><span style="color: #0000BB">?&gt;<br /></span>&lt;/body&gt;<br />&lt;/html&gt;<br /></span>
</code>