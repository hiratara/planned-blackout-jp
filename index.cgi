#!/usr/bin/perl

$VER="V.1.124(nanakochi123456)";
$tarball="power110321.tar.gz";

$history=<<EOM;
<h3>データ更新状況:</h3>
<ul id="update">
<li>2011/3/19 17:08 東京電力データを更新した</li>
</ul>
<a href="http://power.daiba.cx/wiki/?%a5%c7%a1%bc%a5%bf%b9%b9%bf%b7%cd%fa%ce%f2">これ以前の当方のデータ更新履歴</a><br />
<a href="http://bizoole.com/power/history/datahistory.html">これ以前の本家のデータ更新履歴</a>

<h3>エンジン更新履歴:</h3>
<ul id="engine">
<li>2011/3/21 06:30 PC/モバイル別にTOPページを指定できるようにした。(注:update.cgiを更新しています。別途<a href="update.txt">こちら</a>から新たに入手して下さい。)</li>
<li>2011/3/20 19:57 東京電力のtwitterによる発表による、一部グループ見送りの件を追記した。</li>
<li>2011/3/20 13:11 文字入力の所で、例　？丁目等の数字が半角であったのを全角に変換できるようにした。</li>
<li>2011/3/20 06:10 20日も計画停電なしの旨をエンジンに反映</li>
<li>2011/3/19 19:43 Jcode.pm を使用しなくてもよくなるように、Encode wrapper 及び jcode.pl ＆ Jcode.pm から移植した文字コード判別ルーチンを作成した。</li>
<li>2011/3/19 16:18 SSIで.htmlに関連付けされているサーバーでは、header.html、footer.htmlをincludeするようにできるようにしました。DirectoryIndex で index.shtml を優先使用するようにすれば、index.shtml でも使用可能と思われます。</li>
<li>2011/3/19 15:30 ケ を ヶ に変換するようにした。将来使用すると思っていた郵便番号のカナデータを削除した。</LI>
</ul>
<br />
<a href="http://power.daiba.cx/wiki/?%a5%a8%a5%f3%a5%b8%a5%f3%b9%b9%bf%b7%cd%fa%ce%f2">これ以前の当方のエンジン更新履歴</a><br />
<a href="http://bizoole.com/power/history/">これ以前のエンジン更新履歴</a>
EOM

#------------

$mobileflg=0;
$mobileflg=1 if($ENV{HTTP_USER_AGENT}=~/DoCoMo|UP\.Browser|KDDI|SoftBank|Voda[F|f]one|J\-PHONE|DDIPOCKET|WILLCOM|iPod|PDA/);

$mobileflg=0 if($ENV{QUERY_STRING} eq 'p');
$mobileflg=1 if($ENV{QUERY_STRING} eq 'm');

$scriptandcss=<<EOM if ($mobileflg eq 0);
<style type="text/css">
\@charset "UTF-8";
//reset html {
color:#000;
background:#FFF;
}
body, div, dl, dt, dd, ul, ol, li, h1, h2, h3, h4, h5, h6, pre, code, form, fieldset, legend, input, textarea, p, blockquote, th, td {
	margin:0;
	padding:0;
}
table {
	border-collapse:collapse;
	border-spacing:0;
}
fieldset, img {
	border:0;
}
address, caption, cite, code, dfn, em, strong, th, var {
	font-style:normal;
	font-weight:normal;
}
li {
	list-style:none;
}
caption, th {
	text-align:left;
}
h1, h2, h3, h4, h5, h6 {
	font-size:100%;
	font-weight:normal;
}
q:before, q:after {
	content:'';
}
abbr, acronym {
	border:0;
	font-variant:normal;
}
sup {
	vertical-align:text-top;
}
sub {
	vertical-align:text-bottom;
}
input, textarea, select {
	font-family:inherit;
	font-size:inherit;
	font-weight:inherit;
}
input, textarea, select {
*font-size:100%;
}
legend {
	color:#000;
}
body {
	font-size: 16px;
	font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "メイリオ", Meiryo, Osaka, "ＭＳ Ｐゴシック", "MS PGothic", sans-serif;
}
h1 {
	font-size: 1.4em;
	text-align: center;
	margin-bottom: 15px;
	clear: both;
	display: block;
	padding-top: 10px;
}
div#wrapper {
	width: 760px;
	margin-top: 0px;
	margin-right: auto;
	margin-bottom: 0px;
	margin-left: auto;
}
div#sArea {
	/* [disabled]float: left; */
}
div#sAreaL, div#sAreaR {
	width:340px;
	float:left;
	color: #000;
	padding-top: 0;
	padding-right: 15px;
	padding-bottom: 0;
	padding-left: 15px;
}
div#zip {
	width:680px;
	float:left;
	color: #000;
	padding-top: 0;
	padding-right: 15px;
	padding-bottom: 0;
	padding-left: 15px;
}

div#sArea h2 {
	margin-bottom: 6px;
}
ul#otherService {
	margin-top: 20px;
}
ul#otherService li {
	float: left;
}
ul#otherService li a[href] {
	display: block;
	margin-right: 10px;
}
span.h2List {
	color: #F90;
}
div.miList {
	width:50%;
	float:left;
	margin-bottom: 3px;
}
div#sArea {
	padding: 10px;
	background-color: #9DCEF5;
	font-size: 0.9em;
	line-height: 1.6em;
	margin-top: 3px;
	float: left;
}
input#city {
	border-top-style: none;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	padding: 3px;
	width: 100%;
	font-size: 18px;
}
input#zip {
	border-top-style: none;
	border-right-style: none;
	border-bottom-style: none;
	border-left-style: none;
	padding: 3px;
	width: 20%;
	font-size: 18px;
}

p.notice {
	font-size: 0.9em;
	margin-bottom: 10px;
	padding-top: 3px;
	padding-bottom: 3px;
}
div#sAreaR > label {
	display: block;
	float: left;
	margin-right: 10px;
	width: 30%;
}
div#submitArea {
	text-align: center;
	width: 100%;
}
div#submitArea input {
	padding: 5px;
	width: 200px;
	margin-top: 10px;
	margin-right: auto;
	margin-bottom: 0px;
	margin-left: auto;
}
ul#tList li {
	display: block;
	float: left;
	margin-bottom: 5px;
	margin-right: 20px;
	list-style-type: decimal;
	list-style-position: inside;
}
p.designed {
	font-size: 0.7em;
}
ul#thList li {
	margin: 0px;
	padding: 0px;
}
div.mrExp, div.mrHelp {
	width: 95%;
	margin-top: 10px;
	margin-right: auto;
	margin-bottom: 10px;
	margin-left: auto;
	padding: 5px;
	line-height: 1.4em;
	font-size: 0.9em;
}
div.TabbedPanelsContent h3 {
	font-weight: bold;
	text-decoration: underline;
	margin-top: 3px;
	margin-bottom: 3px;
}
ul#update li, ul#engine li, ul#wishList li {
	font-size: 0.9em;
	list-style-position: inside;
	list-style-type: disc;
	margin-left: 1em;
}
p.contact {
	margin-top: 20px;
}
p.notice {
	margin-top: 5px;
	margin-bottom: 5px;
	clear: both;
	float: left;
}
 \@charset "UTF-8";
/* SpryTabbedPanels.css - version 0.6 - Spry Pre-Release 1.6.1 */

/* Copyright (c) 2006. Adobe Systems Incorporated. All rights reserved. */

/* Horizontal Tabbed Panels
 *
 * The default style for a TabbedPanels widget places all tab buttons
 * (left aligned) above the content panel.
 */

/* This is the selector for the main TabbedPanels container. For our
 * default style, this container does not contribute anything visually,
 * but it is floated left to make sure that any floating or clearing done
 * with any of its child elements are contained completely within the
 * TabbedPanels container, to minimize any impact or undesireable
 * interaction with other floated elements on the page that may be used
 * for layout.
 *
 * If you want to constrain the width of the TabbedPanels widget, set a
 * width on the TabbedPanels container. By default, the TabbedPanels widget
 * expands horizontally to fill up available space.
 *
 * The name of the class ("TabbedPanels") used in this selector is not
 * necessary to make the widget function. You can use any class name you
 * want to style the TabbedPanels container.
 */
.TabbedPanels {
	overflow: hidden;
	margin: 0px;
	padding: 0px;
	clear: none;
	width: 100%; /* IE Hack to force proper layout when preceded by a paragraph. (hasLayout Bug)*/
}
/* This is the selector for the TabGroup. The TabGroup container houses
 * all of the tab buttons for each tabbed panel in the widget. This container
 * does not contribute anything visually to the look of the widget for our
 * default style.
 *
 * The name of the class ("TabbedPanelsTabGroup") used in this selector is not
 * necessary to make the widget function. You can use any class name you
 * want to style the TabGroup container.
 */
.TabbedPanelsTabGroup {
	margin: 0px;
	padding: 0px;
}
/* This is the selector for the TabbedPanelsTab. This container houses
 * the title for the panel. This is also the tab "button" that the user clicks
 * on to activate the corresponding content panel so that it appears on top
 * of the other tabbed panels contained in the widget.
 *
 * For our default style, each tab is positioned relatively 1 pixel down from
 * where it wold normally render. This allows each tab to overlap the content
 * panel that renders below it. Each tab is rendered with a 1 pixel bottom
 * border that has a color that matches the top border of the current content
 * panel. This gives the appearance that the tab is being drawn behind the
 * content panel.
 *
 * The name of the class ("TabbedPanelsTab") used in this selector is not
 * necessary to make the widget function. You can use any class name you want
 * to style this tab container.
 */
.TabbedPanelsTab {
	position: relative;
	top: 1px;
	float: left;
	padding: 4px 10px;
	margin: 0px 1px 0px 0px;
	font: bold 0.7em sans-serif;
	background-color: #9DCEF5;
	list-style: none;
	border-left: solid 1px #CCC;
	border-bottom: solid 1px #999;
	border-top: solid 1px #999;
	border-right: solid 1px #999;
	-moz-user-select: none;
	-khtml-user-select: none;
	cursor: pointer;
}
/* This selector is an example of how to change the appearnce of a tab button
 * container as the mouse enters it. The class "TabbedPanelsTabHover" is
 * programatically added and removed from the tab element as the mouse enters
 * and exits the container.
 */
.TabbedPanelsTabHover {
	background-color: #FC0;
}
/* This selector is an example of how to change the appearance of a tab button
 * container after the user has clicked on it to activate a content panel.
 * The class "TabbedPanelsTabSelected" is programatically added and removed
 * from the tab element as the user clicks on the tab button containers in
 * the widget.
 *
 * As mentioned above, for our default style, tab buttons are positioned
 * 1 pixel down from where it would normally render. When the tab button is
 * selected, we change its bottom border to match the background color of the
 * content panel so that it looks like the tab is part of the content panel.
 */
.TabbedPanelsTabSelected {
	background-color: #FFF;
	border-bottom: 1px solid #EEE;
}
/* This selector is an example of how to make a link inside of a tab button
 * look like normal text. Users may want to use links inside of a tab button
 * so that when it gets focus, the text *inside* the tab button gets a focus
 * ring around it, instead of the focus ring around the entire tab.
 */
.TabbedPanelsTab a {
	color: black;
	text-decoration: none;
}
/* This is the selector for the ContentGroup. The ContentGroup container houses
 * all of the content panels for each tabbed panel in the widget. For our
 * default style, this container provides the background color and borders that
 * surround the content.
 *
 * The name of the class ("TabbedPanelsContentGroup") used in this selector is
 * not necessary to make the widget function. You can use any class name you
 * want to style the ContentGroup container.
 */
.TabbedPanelsContentGroup {
	clear: both;
	border-left: solid 1px #CCC;
	border-bottom: solid 1px #CCC;
	border-top: solid 1px #999;
	border-right: solid 1px #999;
	background-color: #FFF;
}
/* This is the selector for the Content panel. The Content panel holds the
 * content for a single tabbed panel. For our default style, this container
 * provides some padding, so that the content is not pushed up against the
 * widget borders.
 *
 * The name of the class ("TabbedPanelsContent") used in this selector is
 * not necessary to make the widget function. You can use any class name you
 * want to style the Content container.
 */
.TabbedPanelsContent {
	overflow: hidden;
	padding-top: 4px;
	padding-right: 14px;
	padding-bottom: 4px;
	padding-left: 14px;
}
/* This selector is an example of how to change the appearnce of the currently
 * active container panel. The class "TabbedPanelsContentVisible" is
 * programatically added and removed from the content element as the panel
 * is activated/deactivated.
 */
.TabbedPanelsContentVisible {
}
/* Vertical Tabbed Panels
 *
 * The following rules override some of the default rules above so that the
 * TabbedPanels widget renders with its tab buttons along the left side of
 * the currently active content panel.
 *
 * With the rules defined below, the only change that will have to be made
 * to switch a horizontal tabbed panels widget to a vertical tabbed panels
 * widget, is to use the "VTabbedPanels" class on the top-level widget
 * container element, instead of "TabbedPanels".
 */

.VTabbedPanels {
	overflow: hidden;
	zoom: 1;
}
/* This selector floats the TabGroup so that the tab buttons it contains
 * render to the left of the active content panel. A border is drawn around
 * the group container to make it look like a list container.
 */
.VTabbedPanels .TabbedPanelsTabGroup {
	float: left;
	width: 10em;
	height: 20em;
	background-color: #FFF;
	position: relative;
	border-top: solid 1px #999;
	border-right: solid 1px #999;
	border-left: solid 1px #CCC;
	border-bottom: solid 1px #CCC;
}
/* This selector disables the float property that is placed on each tab button
 * by the default TabbedPanelsTab selector rule above. It also draws a bottom
 * border for the tab. The tab button will get its left and right border from
 * the TabGroup, and its top border from the TabGroup or tab button above it.
 */
.VTabbedPanels .TabbedPanelsTab {
	float: none;
	margin: 0px;
	border-top: none;
	border-left: none;
	border-right: none;
}
/* This selector disables the float property that is placed on each tab button
 * by the default TabbedPanelsTab selector rule above. It also draws a bottom
 * border for the tab. The tab button will get its left and right border from
 * the TabGroup, and its top border from the TabGroup or tab button above it.
 */
.VTabbedPanels .TabbedPanelsTabSelected {
	background-color: #EEE;
	border-bottom: solid 1px #999;
}
/* This selector floats the content panels for the widget so that they
 * render to the right of the tabbed buttons.
 */
.VTabbedPanels .TabbedPanelsContentGroup {
	clear: none;
	float: left;
	padding: 0px;
	width: 30em;
	height: 20em;
}

/* Styles for Printing */
\@media print {
.TabbedPanels {
	overflow: visible !important;
}
.TabbedPanelsContentGroup {
	display: block !important;
	overflow: visible !important;
	height: auto !important;
}
.TabbedPanelsContent {
	overflow: visible !important;
	display: block !important;
	clear:both !important;
}
.TabbedPanelsTab {
	overflow: visible !important;
	display: block !important;
	clear:both !important;
}
div#TabbedPanels1 {
	/* [disabled]clear: both; */
	/* [disabled]float: left; */
}
</style>
<script type="text/javascript">
// SpryTabbedPanels.js - version 0.7 - Spry Pre-Release 1.6.1
//
// Copyright (c) 2006. Adobe Systems Incorporated.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//   * Redistributions in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//   * Neither the name of Adobe Systems Incorporated nor the names of its
//     contributors may be used to endorse or promote products derived from this
//     software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

(function() { // BeginSpryComponent

if (typeof Spry == "undefined") window.Spry = {}; if (!Spry.Widget) Spry.Widget = {};

Spry.Widget.TabbedPanels = function(element, opts)
{
	this.element = this.getElement(element);
	this.defaultTab = 0; // Show the first panel by default.
	this.tabSelectedClass = "TabbedPanelsTabSelected";
	this.tabHoverClass = "TabbedPanelsTabHover";
	this.tabFocusedClass = "TabbedPanelsTabFocused";
	this.panelVisibleClass = "TabbedPanelsContentVisible";
	this.focusElement = null;
	this.hasFocus = false;
	this.currentTabIndex = 0;
	this.enableKeyboardNavigation = true;
	this.nextPanelKeyCode = Spry.Widget.TabbedPanels.KEY_RIGHT;
	this.previousPanelKeyCode = Spry.Widget.TabbedPanels.KEY_LEFT;

	Spry.Widget.TabbedPanels.setOptions(this, opts);

	// If the defaultTab is expressed as a number/index, convert
	// it to an element.

	if (typeof (this.defaultTab) == "number")
	{
		if (this.defaultTab < 0)
			this.defaultTab = 0;
		else
		{
			var count = this.getTabbedPanelCount();
			if (this.defaultTab >= count)
				this.defaultTab = (count > 1) ? (count - 1) : 0;
		}

		this.defaultTab = this.getTabs()[this.defaultTab];
	}

	// The defaultTab property is supposed to be the tab element for the tab content
	// to show by default. The caller is allowed to pass in the element itself or the
	// element's id, so we need to convert the current value to an element if necessary.

	if (this.defaultTab)
		this.defaultTab = this.getElement(this.defaultTab);

	this.attachBehaviors();
};

Spry.Widget.TabbedPanels.prototype.getElement = function(ele)
{
	if (ele && typeof ele == "string")
		return document.getElementById(ele);
	return ele;
};

Spry.Widget.TabbedPanels.prototype.getElementChildren = function(element)
{
	var children = [];
	var child = element.firstChild;
	while (child)
	{
		if (child.nodeType == 1 /* Node.ELEMENT_NODE */)
			children.push(child);
		child = child.nextSibling;
	}
	return children;
};

Spry.Widget.TabbedPanels.prototype.addClassName = function(ele, className)
{
	if (!ele || !className || (ele.className && ele.className.search(new RegExp("\\\\b" + className + "\\\\b")) != -1))
		return;
	ele.className += (ele.className ? " " : "") + className;
};

Spry.Widget.TabbedPanels.prototype.removeClassName = function(ele, className)
{
	if (!ele || !className || (ele.className && ele.className.search(new RegExp("\\\\b" + className + "\\\\b")) == -1))
		return;
	ele.className = ele.className.replace(new RegExp("\\\\s*\\\\b" + className + "\\\\b", "g"), "");
};

Spry.Widget.TabbedPanels.setOptions = function(obj, optionsObj, ignoreUndefinedProps)
{
	if (!optionsObj)
		return;
	for (var optionName in optionsObj)
	{
		if (ignoreUndefinedProps && optionsObj[optionName] == undefined)
			continue;
		obj[optionName] = optionsObj[optionName];
	}
};

Spry.Widget.TabbedPanels.prototype.getTabGroup = function()
{
	if (this.element)
	{
		var children = this.getElementChildren(this.element);
		if (children.length)
			return children[0];
	}
	return null;
};

Spry.Widget.TabbedPanels.prototype.getTabs = function()
{
	var tabs = [];
	var tg = this.getTabGroup();
	if (tg)
		tabs = this.getElementChildren(tg);
	return tabs;
};

Spry.Widget.TabbedPanels.prototype.getContentPanelGroup = function()
{
	if (this.element)
	{
		var children = this.getElementChildren(this.element);
		if (children.length > 1)
			return children[1];
	}
	return null;
};

Spry.Widget.TabbedPanels.prototype.getContentPanels = function()
{
	var panels = [];
	var pg = this.getContentPanelGroup();
	if (pg)
		panels = this.getElementChildren(pg);
	return panels;
};

Spry.Widget.TabbedPanels.prototype.getIndex = function(ele, arr)
{
	ele = this.getElement(ele);
	if (ele && arr && arr.length)
	{
		for (var i = 0; i < arr.length; i++)
		{
			if (ele == arr[i])
				return i;
		}
	}
	return -1;
};

Spry.Widget.TabbedPanels.prototype.getTabIndex = function(ele)
{
	var i = this.getIndex(ele, this.getTabs());
	if (i < 0)
		i = this.getIndex(ele, this.getContentPanels());
	return i;
};

Spry.Widget.TabbedPanels.prototype.getCurrentTabIndex = function()
{
	return this.currentTabIndex;
};

Spry.Widget.TabbedPanels.prototype.getTabbedPanelCount = function(ele)
{
	return Math.min(this.getTabs().length, this.getContentPanels().length);
};

Spry.Widget.TabbedPanels.addEventListener = function(element, eventType, handler, capture)
{
	try
	{
		if (element.addEventListener)
			element.addEventListener(eventType, handler, capture);
		else if (element.attachEvent)
			element.attachEvent("on" + eventType, handler);
	}
	catch (e) {}
};

Spry.Widget.TabbedPanels.prototype.cancelEvent = function(e)
{
	if (e.preventDefault) e.preventDefault();
	else e.returnValue = false;
	if (e.stopPropagation) e.stopPropagation();
	else e.cancelBubble = true;

	return false;
};

Spry.Widget.TabbedPanels.prototype.onTabClick = function(e, tab)
{
	this.showPanel(tab);
	return this.cancelEvent(e);
};

Spry.Widget.TabbedPanels.prototype.onTabMouseOver = function(e, tab)
{
	this.addClassName(tab, this.tabHoverClass);
	return false;
};

Spry.Widget.TabbedPanels.prototype.onTabMouseOut = function(e, tab)
{
	this.removeClassName(tab, this.tabHoverClass);
	return false;
};

Spry.Widget.TabbedPanels.prototype.onTabFocus = function(e, tab)
{
	this.hasFocus = true;
	this.addClassName(tab, this.tabFocusedClass);
	return false;
};

Spry.Widget.TabbedPanels.prototype.onTabBlur = function(e, tab)
{
	this.hasFocus = false;
	this.removeClassName(tab, this.tabFocusedClass);
	return false;
};

Spry.Widget.TabbedPanels.KEY_UP = 38;
Spry.Widget.TabbedPanels.KEY_DOWN = 40;
Spry.Widget.TabbedPanels.KEY_LEFT = 37;
Spry.Widget.TabbedPanels.KEY_RIGHT = 39;



Spry.Widget.TabbedPanels.prototype.onTabKeyDown = function(e, tab)
{
	var key = e.keyCode;
	if (!this.hasFocus || (key != this.previousPanelKeyCode && key != this.nextPanelKeyCode))
		return true;

	var tabs = this.getTabs();
	for (var i =0; i < tabs.length; i++)
		if (tabs[i] == tab)
		{
			var el = false;
			if (key == this.previousPanelKeyCode && i > 0)
				el = tabs[i-1];
			else if (key == this.nextPanelKeyCode && i < tabs.length-1)
				el = tabs[i+1];

			if (el)
			{
				this.showPanel(el);
				el.focus();
				break;
			}
		}

	return this.cancelEvent(e);
};

Spry.Widget.TabbedPanels.prototype.preorderTraversal = function(root, func)
{
	var stopTraversal = false;
	if (root)
	{
		stopTraversal = func(root);
		if (root.hasChildNodes())
		{
			var child = root.firstChild;
			while (!stopTraversal && child)
			{
				stopTraversal = this.preorderTraversal(child, func);
				try { child = child.nextSibling; } catch (e) { child = null; }
			}
		}
	}
	return stopTraversal;
};

Spry.Widget.TabbedPanels.prototype.addPanelEventListeners = function(tab, panel)
{
	var self = this;
	Spry.Widget.TabbedPanels.addEventListener(tab, "click", function(e) { return self.onTabClick(e, tab); }, false);
	Spry.Widget.TabbedPanels.addEventListener(tab, "mouseover", function(e) { return self.onTabMouseOver(e, tab); }, false);
	Spry.Widget.TabbedPanels.addEventListener(tab, "mouseout", function(e) { return self.onTabMouseOut(e, tab); }, false);

	if (this.enableKeyboardNavigation)
	{
		// XXX: IE doesn't allow the setting of tabindex dynamically. This means we can't
		// rely on adding the tabindex attribute if it is missing to enable keyboard navigation
		// by default.

		// Find the first element within the tab container that has a tabindex or the first
		// anchor tag.
		
		var tabIndexEle = null;
		var tabAnchorEle = null;

		this.preorderTraversal(tab, function(node) {
			if (node.nodeType == 1 /* NODE.ELEMENT_NODE */)
			{
				var tabIndexAttr = tab.attributes.getNamedItem("tabindex");
				if (tabIndexAttr)
				{
					tabIndexEle = node;
					return true;
				}
				if (!tabAnchorEle && node.nodeName.toLowerCase() == "a")
					tabAnchorEle = node;
			}
			return false;
		});

		if (tabIndexEle)
			this.focusElement = tabIndexEle;
		else if (tabAnchorEle)
			this.focusElement = tabAnchorEle;

		if (this.focusElement)
		{
			Spry.Widget.TabbedPanels.addEventListener(this.focusElement, "focus", function(e) { return self.onTabFocus(e, tab); }, false);
			Spry.Widget.TabbedPanels.addEventListener(this.focusElement, "blur", function(e) { return self.onTabBlur(e, tab); }, false);
			Spry.Widget.TabbedPanels.addEventListener(this.focusElement, "keydown", function(e) { return self.onTabKeyDown(e, tab); }, false);
		}
	}
};

Spry.Widget.TabbedPanels.prototype.showPanel = function(elementOrIndex)
{
	var tpIndex = -1;
	
	if (typeof elementOrIndex == "number")
		tpIndex = elementOrIndex;
	else // Must be the element for the tab or content panel.
		tpIndex = this.getTabIndex(elementOrIndex);
	
	if (!tpIndex < 0 || tpIndex >= this.getTabbedPanelCount())
		return;

	var tabs = this.getTabs();
	var panels = this.getContentPanels();

	var numTabbedPanels = Math.max(tabs.length, panels.length);

	for (var i = 0; i < numTabbedPanels; i++)
	{
		if (i != tpIndex)
		{
			if (tabs[i])
				this.removeClassName(tabs[i], this.tabSelectedClass);
			if (panels[i])
			{
				this.removeClassName(panels[i], this.panelVisibleClass);
				panels[i].style.display = "none";
			}
		}
	}

	this.addClassName(tabs[tpIndex], this.tabSelectedClass);
	this.addClassName(panels[tpIndex], this.panelVisibleClass);
	panels[tpIndex].style.display = "block";

	this.currentTabIndex = tpIndex;
};

Spry.Widget.TabbedPanels.prototype.attachBehaviors = function(element)
{
	var tabs = this.getTabs();
	var panels = this.getContentPanels();
	var panelCount = this.getTabbedPanelCount();

	for (var i = 0; i < panelCount; i++)
		this.addPanelEventListeners(tabs[i], panels[i]);

	this.showPanel(this.defaultTab);
};

})(); // EndSpryComponent

</script>

<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
EOM

$top=<<EOM;
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="ja" />
<title>計画停電時間検索 | 停電グループや停電時間を検索できるツール</title>
<meta name="description" content="計画停電の時間やグループを検索できるツールです。市区町村名、地域名など住所の一部や郵便番号などから停電時間を検索できます。">
<meta name="keywords" content="計画停電,検索,システム,ツール,スケジュール,輪番停電,グループ">$scriptandcss
</head>
<body>
EOM

$mobile_body=<<EOM;
$VER
<!include="header.html">
<table border="1"><tr><td>
<strong>停電時間検索ツール</strong><br />
(東京電力、東北電力)<br /><br />
計画停電（輪番停電）の時間やグループを簡単に検索できるツールです。<br />自分の住んでいる地域がどこのグループに属するのか、住所の一部などから検索できます。<br /><a href="?p">PC向けページ</a>
<br />
<form action="area.cgi" method="get">
    計画停電の予定時間を知りたい市区町村名、地域名<input type="text" name="city" size="20" istyle="1" mode="hiragana" style="ime-mode: active;"/>
<input type="submit" name="submit" value="検索" /><br />
    または郵便番号<input type="text" name="zip1" maxlength="3" size="3" istyle="4" mode="numeric" style="ime-mode:disabled;" />-<input type="text" name="zip2" maxlength="4" size="4" istyle="4" mode="numeric" style="ime-mode:disabled;" />
<input type="submit" name="submit" value="検索" /><br />
　　グループ番号で絞り込み<select name="gid">
	<option value="0">指定なし</option>
	<option value="1">グループ1</option>
	<option value="2">グループ2</option>
	<option value="3">グループ3</option>
	<option value="4">グループ4</option>
	<option value="5">グループ5</option>
	<option value="6">グループ6(東北のみ)</option>
	<option value="7">グループ7(東北のみ)</option>
	<option value="8">グループ8(東北のみ)</option>
	</select></form>
*Area search and summary of Planned blackout is following link. <a href="http://inferno.soutan.net/power/search">For English</a>
</td></tr></table>
<table border="0">
<tr><td colspan="2">
アクセス集中でService Temporarily Unavailable表示をすることがあります。ミラーサーバをご利用ください。</td></tr>
<tr><td colspan="2">
<a href="http://denki.moene.ws/?list">全ミラー/機能拡張サーバ 全リスト(67サイト)</a>
ミラーサーバや本家よりさらに独自機能を搭載したサーバのご協力をいただいている67サイトの方々に感謝いたします。<br /></td></tr>
<tr><td colspan="2">どのサーバを使うか悩んだときは、負荷分散機能を持つ<a href="http://denki.moene.ws/">http://denki.moene.ws/</a>(tnx:Kei_Nanigashi)や<a href="http://bit.ly/e6b2XL">http://bit.ly/e6b2XL</a>(tnx:_nat)をご利用ください。<br /></td></tr>
</table>
問い合わせは、<a href="http://twitter.com/mnakajim">twitter (\@mnakajim)</a>へ<BR><br>
<hr />
<!include="footer.html">
<a href=http://bizoole.com/power>計画停電時間検索ツール</a>本家サイトへ　　原作:<a href=http://twitter.com/mnakajim/>中島昌彦</a>(M.NAKAJIM)<br>
<br>
special tnx:10b346(by SEO)
</body>
</html>

EOM

$pc_body=<<EOM;
<body>
<div id="wrapper">
<h1>停電時間検索 $VER (東京電力、東北電力)</h1>
<!include="header.html">
計画停電の時間やグループを検索できるツールです。<br />東京電力、東北電力の公式データを元にしています。<br>
<a href="?m">モバイル向けページ</a>
<div id="sArea">
計画停電（輪番停電）の時間やグループを簡単に検索できるツールです。
自分の住んでいる地域がどこのグループに属するのか、住所の一部などから検索できます。
<form action="./area.cgi" method="get">
<div id="sAreaL">
<h2><span class="h2List">▶</span>計画停電の予定時間を知りたい市区町村名、地域名</h2>
<input type="text" name="city" size="20" id="city" />
</div>
<div id="sAreaR">
<h2><span class="h2List">▶</span>グループ番号で絞り込み</h2>
<label>
<input name="gid" type="radio" value="0" />
指定なし</label>
<label>
<input name="gid" type="radio" value="1" />
グループ1</label>
<label>
<input name="gid" type="radio" value="2" />
グループ2</label>
<label>
<input name="gid" type="radio" value="3" />
グループ3</label>
<label>
<input name="gid" type="radio" value="4" />
グループ4</label>
<label>
<input name="gid" type="radio" value="5" />
グループ5</label>
</div>
<div id="zip">
<h2><span class="h2List">▶</span>もしくは郵便番号で検索する。</h2>
<input type="text" name="zip1" maxlength="3" size="3" istyle="4" mode="numeric" style="ime-mode:disabled;" id="zip" />－<input type="text" name="zip2" maxlength="4" size="4" istyle="4" mode="numeric" style="ime-mode:disabled;" id="zip" />
</div>
<div style="clear:both;" id="submitArea">
<input type="submit" name="submit" value="検索" />
</div>
</form>
<ul id="otherService">
<li>その他のサービス：</li>
<li><a href="http://inferno.soutan.net/power/search">for English(fivewits SAN)</a></li>
</ul>
</div>
<p class="notice"></p>
<div id="TabbedPanels1" class="TabbedPanels">
<ul class="TabbedPanelsTabGroup">
<li class="TabbedPanelsTab" tabindex="0">ミラーリスト1</li>
<li class="TabbedPanelsTab" tabindex="0">ミラーリスト2</li>
<li class="TabbedPanelsTab" tabindex="0">ミラーリスト3</li>
<li class="TabbedPanelsTab" tabindex="0">ミラーリスト4</li>
<li class="TabbedPanelsTab" tabindex="0">データ更新状況</li>
<li class="TabbedPanelsTab" tabindex="0">API/機能強化</li>
<li class="TabbedPanelsTab" tabindex="0">Special Thanks</li>
</ul>
<div class="TabbedPanelsContentGroup"> 
<!-- tab 1 //-->
<div class="TabbedPanelsContent">
<h3>ミラーサーバーご協力（順不同）</h3>
<div class="mrExp">どのサーバを使うか悩んだときは、負荷分散機能を持つ<a href="http://denki.moene.ws/">http://denki.moene.ws/</a>(tnx:Kei_Nanigashi)や<a href="http://bit.ly/e6b2XL">http://bit.ly/e6b2XL</a>(tnx:_nat)をご利用ください。<br>
<a href="http://denki.moene.ws/?list">全ミラー/機能拡張サーバ 全リスト(70サイト)</a></div>
<ul>
<li class="miList"><a href="http://bizoole.com/power/">http://bizoole.com/power/</a> (マスタサイト:\@mnakajim)</li>
<li class="miList"><a href="http://kaji.com/p/">http://kaji.com/p/</a> (\@kajimoe)</li>
<li class="miList"><a href="" herf="http://kajisoft.jp/power/">http://kajisoft.jp/power/</a> (\@kajimoe)</li>
<li class="miList"><a href="http://power-failure.xii.jp/">http://power-failure.xii.jp/</a> (\@shall_rappy)</li>
<li class="miList"><a href="http://power.ckin.jp/">http://power.ckin.jp/</a>(\@ckin_tweets)</li>
<li class="miList"><a href="http://area-jp.net/power/">http://area-jp.net/power/</a> (\@nontan333)</li>
<li class="miList"><a href="http://entame-kiti.com/">http://entame-kiti.com/</a> (\@nontan333)</li>
<li class="miList"><a href="http://www.shiti-official.com/power/">http://www.shiti-official.com/power/</a> (\@nontan333)</li>
<li class="miList"><a href="http://www.yun-official.com/power/">http://www.yun-official.com/power/</a> (\@nontan333)</li>
<li class="miList"><a href="http://ynk5.org/teiden/">http://ynk5.org/teiden/</a> (\@Fukushist)</li>
<li class="miList"><a href="http://namuris.period3.to/kt/">http://namuris.period3.to/kt/</a> (\@hidaka)</li>
<li class="miList"><a href="http://sd.pot.co.jp/pub/kt/">http://sd.pot.co.jp/pub/kt/</a> (\@hidakat)</li>
<li class="miList"><a href="http://ruca.crap.jp/power/">http://ruca.crap.jp/power/</a> (\@eteranran)</li>
<li class="miList"><a href="http://www.t-j-k.ne.jp/power/">http://www.t-j-k.ne.jp/power/</a> (\@nontan333)</li>
<li class="miList"><a href="http://keikakuteiden.info/">http://keikakuteiden.info/</a> (\@nao_z)</li>
<li class="miList"><a href="http://arukansoft.net/power/">http://arukansoft.net/power/</a> (\@arukakan)</li>
<li class="miList"><a href="http://pfj.sunnyday-server.net/power110315/">http://pfj.sunnyday-server.net/power110315/</a> (\@papiko583)</li>
<li class="miList"><a href="http://sahiro.org/power/">http://sahiro.org/power/</a> (\@sahiro)</li>
<li class="miList"><a href="http://power.shonantech.com/">http://power.shonantech.com/</a> (\@yabe321)</li>
<li class="miList"><a href="http://www.perutake.com/power/">http://www.perutake.com/power/</a> (\@perutake)</li>
</ul>
<div style="clear:both"></div>
<div class="mrHelp">ミラーサーバのご協力をいただいている上記方々に感謝いたします。</div>
</div>
<div class="TabbedPanelsContent">
<h3>ミラーサーバーご協力（順不同）</h3>
<div class="mrExp">どのサーバを使うか悩んだときは、負荷分散機能を持つ<a href="http://denki.moene.ws/">http://denki.moene.ws/</a>(tnx:Kei_Nanigashi)や<a href="http://bit.ly/e6b2XL">http://bit.ly/e6b2XL</a>(tnx:_nat)をご利用ください。</div>
<ul>
<li class="miList"><a href="http://p.eos1.us/">http://p.eos1.us/</a> (\@eos1)</li>
<li class="miList"><a href="http://watt.dip.jp/power/">http://watt.dip.jp/power/</a> (\@watt_siphon)</li>
<li class="miList"><a href="">http://www.win-road.jp/power/</a> (\@loh_syndrome)</li>
<li class="miList"><a href="http://sakumamamoru.jp/teiden/">http://sakumamamoru.jp/teiden/</a> (\@Komotoya)</li>
<li class="miList"><a href="http://www.rev4.net/power/">http://www.rev4.net/power/</a> (\@misa_kichi)</li>
<li class="miList"><a href="http://helpjapan.jpn.com/power/">http://helpjapan.jpn.com/power/</a> (\@HELPJAPANJPNCOM)</li>
<li class="miList"><a href="http://tomodati.crazyworks.net/">http://tomodati.crazyworks.net/</a> (\@Takumi_Daddy)</li>
<li class="miList"><a href="http://mt-seo.jp/">http://mt-seo.jp/</a> (\@13_yousuke)</li>
<li class="miList"><a href="http://power.moene.ws/">http://power.moene.ws/</a> (3サーバ分散運用:@Kei_Nanigashi)</li>
<li class="miList"><a href="http://kgbu.sakura.ne.jp/power/">http://kgbu.sakura.ne.jp/power/</a> (\@ocaokgbu)</li>
<li class="miList"><a href="http://asdf.homeunix.net/power/">http://asdf.homeunix.net/power/</a> (\@sigemasa)</li>
<li class="miList"><a href="http://www23403u.sakura.ne.jp/power/">http://www23403u.sakura.ne.jp/power/</a> (\@usomillp)</li>
<li class="miList"><a href="http://www.lani-kai.sakura.ne.jp/power/">http://www.lani-kai.sakura.ne.jp/power/</a> (\@lanikai_online)</li>
<li class="miList"><a href="http://winwin7s.com/blackout/">http://winwin7s.com/blackout/</a> (\@kojou279)</li>
<li class="miList"><a href="http://jukai.jp/cgi/teiden/">http://jukai.jp/cgi/teiden/</a> (\@jukaimaeda)</li>
<li class="miList"><a href="http://power.ifos.jp/">http://power.ifos.jp/</a> (\@wargrick)</li>
<li class="miList"><a href="http://phoenix.xtr.jp/power/">http://phoenix.xtr.jp/power/</a> (\@hououdou)</li>
<li class="miList"><a href="http://power.mirror.matsuoka.sh/">http://power.mirror.matsuoka.sh/</a> (\@matsuokanaoki)</li>
<li class="miList"><a href="http://mohawk.sakura.ne.jp/power/">http://mohawk.sakura.ne.jp/power/</a> (\@stingraze)</li>
<li class="miList"><a href="http://teagin.com/power/">http://teagin.com/power/</a> (\@teagin)</li>
<li class="miList"><a href="http://p.takashi.me/">http://p.takashi.me/</a> (\@TakashiChi_ba)</li>
</ul>
<div class="mrHelp">ミラーサーバのご協力をいただいている上記方々に感謝いたします。</div>
</div>
<div class="TabbedPanelsContent">
<h3>ミラーサーバーご協力（順不同）</h3>
<div class="mrExp">どのサーバを使うか悩んだときは、負荷分散機能を持つ<a href="http://denki.moene.ws/">http://denki.moene.ws/</a>(tnx:Kei_Nanigashi)や<a href="http://bit.ly/e6b2XL">http://bit.ly/e6b2XL</a>(tnx:_nat)をご利用ください。</div>
<ul>
<li class="miList"><a href="http://tribalepic.ddo.jp/power/">http://tribalepic.ddo.jp/power/</a> (\@basswo)</li>
<li class="miList"><a href="http://power.daiba.cx/">http://power.daiba.cx/</a> (\@nanakochi123456)</li>
<li class="miList"><a href="http://denx.dip.jp/power/">http://denx.dip.jp/power/</a> (\@yukimasa)</li>
<li class="miList"><a href="http://power.eos1.net/">http://power.eos1.net/</a> (\@eos1)</li>
<li class="miList"><a href="http://www.gtaku.com/power110314/">http://www.gtaku.com/power110314/</a> (\@YAK0U)</li>
<li class="miList"><a href="http://denki.tukaenai.info/">http://denki.tukaenai.info/</a> (\@fabled10)</li>
<li class="miList"><a href="http://historiae.jp/power/">http://historiae.jp/power/</a> (\@historiaejp)</li>
<li class="miList"><a href="http://power.uzuki.ac/">http://power.uzuki.ac/</a> (\@try_uzuki)</li>
<li class="miList"> <a href="http://saigai-info.jp/teiden/">http://saigai-info.jp/teiden/</a> (\@nyatakasan)</li>
<li class="miList"><a href="http://rmix.biz/power/">http://rmix.biz/power/</a> (\@iRSS)</li>
<li class="miList"><a href="http://www.uzula-island.com/power/">http://www.uzula-island.com/power/</a></li>
<li class="miList"><a href="http://power.siter.jp/">http://power.siter.jp/</a> (\@aratafuji)</li>
<li class="miList"><a href="http://power.cozecho.com/">http://power.cozecho.com/</a> (\@yuki777)</li>
<li class="miList"><a href="http://teiden.prayforjpn.info/">http://teiden.prayforjpn.info/</a> (\@berero)</li>
<li class="miList"><a href="http://sahiro.org/power/">http://sahiro.org/power/</a> (\@sahiro)</li>
<li class="miList"><a href="http://yon.or.tv/power/">http://yon.or.tv/power/</a> (\@yonortv)</li>
<li class="miList"><a href="http://rejista.jp/power/">http://rejista.jp/power/</a> (\@kneasKH)</li>
<li class="miList"><a href="http://xi42.sakura.ne.jp/tk/mirror/power/">http://xi42.sakura.ne.jp/tk/mirror/power/</a> (\@xi42_sakura)</li>
<li class="miList"><a href="http://www.al-tiida.co.jp/power/">http://www.al-tiida.co.jp/power/</a> (\@shoji0818)</li>
<li class="miList"><a href="http://www.gosoudan.com/power/">http://www.gosoudan.com/power/</a> (\@_nat)</li>
<li class="miList"><a href="http://www4.atpages.jp/~jirou/power/">http://www4.atpages.jp/~jirou/power/</a></li>
</ul>
<div class="mrHelp">ミラーサーバのご協力をいただいている上記方々に感謝いたします。</div>
</div>
<div class="TabbedPanelsContent">
<h3>ミラーサーバーご協力（順不同）</h3>
<div class="mrExp">どのサーバを使うか悩んだときは、負荷分散機能を持つ<a href="http://denki.moene.ws/">http://denki.moene.ws/</a>(tnx:Kei_Nanigashi)や<a href="http://bit.ly/e6b2XL">http://bit.ly/e6b2XL</a>(tnx:_nat)をご利用ください。</div>
<ul>
<li class="miList"><a href="http://power.sahiro.org/">http://power.sahiro.org/</a> (\@sahiro)</li>
<li class="miList"><a href="http://yamada-t.sakura.ne.jp/power/">http://yamada-t.sakura.ne.jp/power/</a> (\@suchiyanaoyuki)</li>
<li class="miList"><a href="http://www.kzta.net/power/">http://www.kzta.net/power/</a> (\@kzzt)</li>
<li class="miList"><a href="http://www25.atpages.jp/fizblog/">http://www25.atpages.jp/fizblog/</a> (\@Fiz_Mutter)</li>
<li class="miList"><a href="http://www.suzukazekai.com/power/">http://www.suzukazekai.com/power/</a> (\@rnmitsu)</li>
<li class="miList"><a href="http://www.kandabako.info/~power/">http://www.kandabako.info/~power/</a> (\@kandabako)</li>
<li class="miList"><a href="http://otomegokoro.net/power/">http://otomegokoro.net/power/</a> (\@Tonbi_ko)</li>
<li class="miList"><a href="http://www.sf-dream.com/cgi/power/">http://www.sf-dream.com/cgi/power/</a> (\@dream945)</li>
<li class="miList"><a href="http://itnews.jp/power">http://itnews.jp/power</a> (\@itnews_jp)</li>
<li class="miList"><a href="http://www.babirubabe.net/power">http://www.babirubabe.net/power</a> (feepepper)</li>
</ul>
<div class="mrHelp">ミラーサーバのご協力をいただいている上記方々に感謝いたします。</div>
</div>
<!--// tab 1 --> 
<!-- tab 2 //-->
<div class="TabbedPanelsContent">
$history
</div>
<!--// tab 2 --> 
<!-- tab 3 //-->
<div class="TabbedPanelsContent">
<h3>API:</h3>
<ul id="wishList">
<li><a href="http://saigai-info.jp/teiden/api.html">http://saigai-info.jp/teiden/api.html</a>(<a href="http://twitter.com/nyatakasan">nyatakasan</a>)</li>
</ul>
<h3>アイコン素材:</h3>
<ul id="wishList">
<li><a href="http://www.kandabako.info/~power/teiden_icons/">http://www.kandabako.info/~power/teiden_icons/</a>(<a href="http://twitter.com/kandabako">kandabako</a>)</li>
</ul>
</div>
<!--// tab 3 --> 
<!-- tab 4 //-->
<div id="tList" class="TabbedPanelsContent">
<h3>サイトを案内いただきました。ありがとうございます:</h3>
<h4>on twitter (so many follower...)</h4>
<ul id="thList">
<li><a href="http://forum.hangame.co.jp/thread/read.nhn?threadno=666879">http://forum.hangame.co.jp/thread/read.nhn?threadno=666879</a>(tnx:nanakochi123456)</li>
<li><a href="http://blog.hangame.co.jp/nanakkochi/article/34446372/">http://blog.hangame.co.jp/nanakkochi/article/34446372/</a>(tnx:nanakochi123456)</li>
<li><a href="http://ameblo.jp/mirin-bosi/entry-10830485352.html">http://ameblo.jp/mirin-bosi/entry-10830485352.html</a>(tnx:Mrin_bosi)</li>
<li><a href="http://bit.ly/ehnaHX">http://bit.ly/ehnaHX</a>(tnx:redvip)</li>
<li><a href="http://rootless.jp/prayforjapan/">http://rootless.jp/prayforjapan/</a>(tnx:modan)</li>
<li><a href="http://www.geocities.jp/saveeq311/">http://www.geocities.jp/saveeq311/</a>(tnx:masyatam)</li>
<li><a href="http://0324.jp/teiden/">http://0324.jp/teiden/</a>(tnx:tetsu0324)</li>
<li><a href="http://akko.dousetsu.com/teiden.html">http://akko.dousetsu.com/teiden.html</a>(tnx:pgyaaaayk)</li>
<li><a href="http://1341398.info/">http://1341398.info/</a>(tnx:hetyowiz)</li>
<li><a href="http://www43.atwiki.jp/togekikaku/pages/25.html">http://www43.atwiki.jp/togekikaku/pages/25.html</a>(tnx:shrmrkm) </li>
</ul>
<!--// media --> 
</div>
<!--// tab 4 --> 
</div>
</div>
<hr />
<!include="footer.html">
<p>当サイト版の<a href="http://power.daiba.cx/$tarball">ファイルセット</a>あります。サイトの機能強化・運営強化にご協力いただける方、ご利用ください。
<p class="contact">オリジナル・運営:<a href="http://twitter.com/mnakajim">中島昌彦</a>(M.NAKAJIM)</p>
<p>本家サイトへ <a href="http://bizoole.com/power/">停電時間検索ツール</a>
<p class="designed">Supported by<br>
　<a href="http://twitter.com/Komotoya">古本篤史&nbsp;&lt;on twitter&gt;</a>(by toppage design)<br>
　10b346(by SEO)<br>
</p>
</div>
<script type="text/javascript">
var TabbedPanels1 = new Spry.Widget.TabbedPanels("TabbedPanels1");
</script>
</body>
</html>
EOM

#-- gzip圧縮

$gzip_command="gzip";

foreach(split(/:/,$ENV{PATH})) {
	if(-x "$_/$gzip_command") {
		$gzip_path="$_/$gzip_command" ;
		if(open(PIPE,"$::gzip_path --help 2>&1|")) {
			foreach(<PIPE>) {
				$forceflag="--force" if(/(\-\-force)/);
				$fastflag="--fast" if(/(\-\-fast)/);
			}
			close(PIPE);
		}
	}
}
$gzip_path="$gzip_path $fastflag $forceflag";
if ($gzip_path ne '') {
	if(($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/)) {
		if($ENV{'HTTP_ACCEPT_ENCODING'}=~/x-gzip/) {
			$gzip_header="Content-Encoding: x-gzip\n";
		} else {
			$gzip_header="Content-Encoding: gzip\n";
		}
	}
}

#-- サーバー出力
print <<END;
Content-type: text/html; charset=utf-8
END

print "$gzip_header" if($gzip_header ne '');
print "\n";

if ($gzip_header ne '') {
	open(STDOUT,"| $gzip_path");
	binmode(STDOUT);
}

if($mobileflg) {
	$body=$mobile_body;
} else {
	$body=$pc_body;
}

$bodys="";
foreach $line(split(/\n/,$body)) {
	if($line=~/\<\!include\=\"(.+)\.html\"\>/) {
		if(open(R,"$1.html")) {
			$data="";
			foreach(<R>) {
				$data.=$_;
			}
			close(R);
		}
		$bodys.="$data\n";
	} else {
		$bodys.="$line\n";
	}
}

print "$top\n$bodys\n";

close(STDOUT);
