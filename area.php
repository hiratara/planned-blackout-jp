<code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br /></span><span style="color: #FF8000">/*&nbsp;<br />*&nbsp;停電時間検索PHP版<br />*<br />*&nbsp;@mnakajim&nbsp;の&nbsp;perl&nbsp;版を&nbsp;PHP&nbsp;に移植&nbsp;<br />*&nbsp;@author&nbsp;&nbsp;@_nat<br />*&nbsp;@version&nbsp;1.00<br />*<br />*&nbsp;DATA/all.all&nbsp;を読み込んで使います。<br />*&nbsp;<br />*&nbsp;INSTALL<br />*&nbsp;1.&nbsp;このスクリプト&nbsp;http://www.gosoudan.com/power/area.phps&nbsp;を<br />*&nbsp;&nbsp;&nbsp;&nbsp;ダウンロード、拡張子を.php&nbsp;に変更して配置する。<br />*&nbsp;2.&nbsp;http://www.gosoudan.com/power/DATA/all.all&nbsp;をダウンロードし、<br />*&nbsp;&nbsp;&nbsp;&nbsp;area.php&nbsp;をインストールしたフォルダの下にDATAフォルダを作り、<br />*&nbsp;&nbsp;&nbsp;&nbsp;その中に配置する。<br />*/<br /></span><span style="color: #0000BB">$getcity</span><span style="color: #007700">=</span><span style="color: #0000BB">$_REQUEST</span><span style="color: #007700">[</span><span style="color: #DD0000">'city'</span><span style="color: #007700">];<br /></span><span style="color: #0000BB">$getcity</span><span style="color: #007700">=</span><span style="color: #0000BB">preg_replace</span><span style="color: #007700">(</span><span style="color: #DD0000">'/w+/'</span><span style="color: #007700">,</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #0000BB">$getcity</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">=</span><span style="color: #0000BB">$_REQUEST</span><span style="color: #007700">[</span><span style="color: #DD0000">'gid'</span><span style="color: #007700">];<br />if&nbsp;(</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">&gt;</span><span style="color: #0000BB">5&nbsp;</span><span style="color: #007700">||&nbsp;</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">&lt;=</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;<br />}<br /><br /></span><span style="color: #0000BB">$t1&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">strtotime</span><span style="color: #007700">(</span><span style="color: #DD0000">'2011-03-15'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$t2&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">strtotime</span><span style="color: #007700">(</span><span style="color: #DD0000">'2011-03-28'</span><span style="color: #007700">);<br /><br /></span><span style="color: #0000BB">$dd&nbsp;</span><span style="color: #007700">=&nbsp;(</span><span style="color: #0000BB">$t2&nbsp;</span><span style="color: #007700">-&nbsp;</span><span style="color: #0000BB">$t1</span><span style="color: #007700">)&nbsp;/&nbsp;(</span><span style="color: #0000BB">3600</span><span style="color: #007700">*</span><span style="color: #0000BB">24</span><span style="color: #007700">);<br /><br /><br /></span><span style="color: #0000BB">$s</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00,&nbsp;16:50-20:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">);<br /><br /></span><span style="color: #0000BB">$grp</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'06:20-10:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$g16</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00,&nbsp;16:50-20:30'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$g17</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00,&nbsp;16:50-20:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$g18</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'09:20-13:00,&nbsp;16:50-20:30'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,&nbsp;</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$g19</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,</span><span style="color: #DD0000">'09:20-13:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$g20</span><span style="color: #007700">=array(</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #DD0000">'15:20-19:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'18:20-22:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'06:20-10:00,&nbsp;13:50-17:30'</span><span style="color: #007700">,</span><span style="color: #DD0000">'09:20-13:00'</span><span style="color: #007700">,</span><span style="color: #DD0000">'12:20-16:00'</span><span style="color: #007700">);<br /><br /></span><span style="color: #0000BB">$file</span><span style="color: #007700">=</span><span style="color: #0000BB">file</span><span style="color: #007700">(</span><span style="color: #DD0000">"DATA/all.all"</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">$count</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;<br /></span><span style="color: #0000BB">$nr</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">count</span><span style="color: #007700">(</span><span style="color: #0000BB">$file</span><span style="color: #007700">);<br />for(</span><span style="color: #0000BB">$i</span><span style="color: #007700">=</span><span style="color: #0000BB">0</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">&lt;</span><span style="color: #0000BB">$nr</span><span style="color: #007700">;</span><span style="color: #0000BB">$i</span><span style="color: #007700">++)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$line</span><span style="color: #007700">=</span><span style="color: #0000BB">$file</span><span style="color: #007700">[</span><span style="color: #0000BB">$i</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$area&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">preg_split</span><span style="color: #007700">(</span><span style="color: #DD0000">'/\t/'</span><span style="color: #007700">,</span><span style="color: #0000BB">$line</span><span style="color: #007700">);<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$num&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">3</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">=</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">0</span><span style="color: #007700">].</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">1</span><span style="color: #007700">].</span><span style="color: #0000BB">$area</span><span style="color: #007700">[</span><span style="color: #0000BB">2</span><span style="color: #007700">];<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">=</span><span style="color: #0000BB">preg_replace</span><span style="color: #007700">(</span><span style="color: #DD0000">'/&nbsp;/'</span><span style="color: #007700">,</span><span style="color: #DD0000">''</span><span style="color: #007700">,</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">);<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(</span><span style="color: #0000BB">$count&nbsp;</span><span style="color: #007700">%&nbsp;</span><span style="color: #0000BB">2&nbsp;</span><span style="color: #007700">==</span><span style="color: #0000BB">0</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$bgcolor</span><span style="color: #007700">=</span><span style="color: #DD0000">'EEFFFF'</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$bgcolor</span><span style="color: #007700">=</span><span style="color: #DD0000">'FFEEFF'</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(</span><span style="color: #0000BB">preg_match</span><span style="color: #007700">(</span><span style="color: #DD0000">'/$getcity/'</span><span style="color: #007700">,</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">)&nbsp;&amp;&amp;&nbsp;</span><span style="color: #0000BB">$num</span><span style="color: #007700">==</span><span style="color: #0000BB">$getgroup</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">.=</span><span style="color: #DD0000">"&lt;tr&nbsp;bgcolor=$bgcolor&gt;&lt;td&gt;&lt;b&gt;$area1&nbsp;$area2&nbsp;$area3&lt;/b&gt;&lt;/td&gt;&lt;td&gt;$g18[$num]&lt;/td&gt;&lt;td&gt;$g19[$num]&lt;/td&gt;&lt;td&gt;$g20[$num]&lt;/td&gt;&lt;td&gt;第$numグループ&lt;/td&gt;&lt;/tr&gt;\n"</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$count</span><span style="color: #007700">++;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br />&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(</span><span style="color: #0000BB">preg_match</span><span style="color: #007700">(</span><span style="color: #DD0000">"/$getcity/"</span><span style="color: #007700">,</span><span style="color: #0000BB">$areaorg</span><span style="color: #007700">))&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #FF8000">//&nbsp;echo&nbsp;$getcity&nbsp;.&nbsp;":"&nbsp;.&nbsp;$areaorg&nbsp;.":".&nbsp;$num&nbsp;.&nbsp;&nbsp;"&lt;br&gt;\n";<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$num</span><span style="color: #007700">=</span><span style="color: #0000BB">rtrim</span><span style="color: #007700">(</span><span style="color: #0000BB">$num</span><span style="color: #007700">);<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">.=</span><span style="color: #DD0000">"&lt;tr&nbsp;bgcolor=$bgcolor&gt;&lt;td&gt;&lt;b&gt;$area[0]&nbsp;$area[1]&nbsp;$area[2]&lt;/b&gt;&lt;/td&gt;&lt;/td&gt;&lt;td&gt;$g18[$num]&lt;/td&gt;&lt;td&gt;$g19[$num]&lt;/td&gt;&lt;td&gt;$g20[$num]&lt;/td&gt;&lt;td&gt;第&nbsp;$num&nbsp;グループ&lt;/td&gt;&lt;/tr&gt;\n"</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$count</span><span style="color: #007700">++;<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br />&nbsp;&nbsp;&nbsp;&nbsp;}<br />}<br /><br />if&nbsp;(!</span><span style="color: #0000BB">$count</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">=</span><span style="color: #DD0000">"&lt;tr&gt;&lt;td&nbsp;colspan=5&gt;計画停電のないエリアです。&lt;/td&gt;&lt;/tr&gt;"</span><span style="color: #007700">;<br />}<br />if&nbsp;(</span><span style="color: #0000BB">$count</span><span style="color: #007700">&gt;</span><span style="color: #0000BB">40</span><span style="color: #007700">)&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #0000BB">$buf</span><span style="color: #007700">=</span><span style="color: #DD0000">"&lt;tr&gt;&lt;td&nbsp;colspan=5&gt;該当地域が多すぎです。詳細の地域名を入力してください。&lt;/td&gt;&lt;/tr&gt;"</span><span style="color: #007700">;<br />}<br /></span><span style="color: #0000BB">header</span><span style="color: #007700">(</span><span style="color: #DD0000">"Content-type:&nbsp;text/html;charset=utf-8"</span><span style="color: #007700">);<br /></span><span style="color: #0000BB">?&gt;<br /></span>&lt;html&gt;<br />&lt;head&gt;<br />&lt;title&gt;検索結果&lt;/title&gt;<br />&lt;meta&nbsp;name="viewport"&nbsp;content="width=device-width,&nbsp;initial-scale=1,&nbsp;maximum-scal<br />e=1"&gt;<br />&lt;/head&gt;<br />&lt;body&gt;<br />&lt;h1&nbsp;style="background-color:#ffdddd;border-left:15px&nbsp;#FFAAAA&nbsp;solid;"&gt;<br />停電時間検索結果&lt;/h1&gt;<br /><span style="color: #0000BB">&lt;?=$count?&gt;</span>件が見つかりました。同一地域で複数登録があるときは、場所によって予定時間が異なります。&lt;BR&gt;<br />1日2回の停電予定がある場合、後半の停電予定は状況に応じて実行となります。<br />&lt;table&nbsp;border=1&gt;&lt;tr&nbsp;bgcolor=#C0C0C0&gt;&lt;th&gt;地域&lt;/th&gt;&lt;th&gt;18日停電時間&lt;/th&gt;&lt;th&gt;19日停電時間&lt;/th&gt;&lt;th&gt;20日停電時間&lt;/th&gt;&lt;th&gt;グループ&lt;/th&gt;&lt;/tr&gt;<br /><span style="color: #0000BB">&lt;?=$buf?&gt;<br /></span>&lt;/table&gt;&lt;a&nbsp;href=./index2.html&gt;戻る&lt;/a&gt;<br />&lt;/body&gt;<br />&lt;/html&gt;<br /></span>
</code>