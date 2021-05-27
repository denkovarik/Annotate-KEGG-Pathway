var MSIE, Netscape, Opera, Safari, Firefox, Chrome;

if(window.navigator.appName.indexOf("Internet Explorer") >= 0){
	MSIE = true;
}else if(window.navigator.appName == "Opera"){
	Opera = true;
}else if(window.navigator.userAgent.indexOf("Chrome") >= 0){
	Chrome = true;
}else if(window.navigator.userAgent.indexOf("Safari") >= 0){
	Safari = true;
}else if(window.navigator.userAgent.indexOf("Firefox") >= 0){
	Firefox = true;
	Netscape = true;
}else{
	Netscape = true;
}

//-------------------------------------------------------------
// ���󥹥ȥ饯��
//-------------------------------------------------------------
function Component(id)
{
	this._component = document.getElementById(id);
	this._opacity_change_interval = 1;
	
	var opc = this._component.style.opacity;
	if(opc == "")
	{
		opc = 1;
	}
	this._opacity = opc * 100;
}


//-------------------------------------------------------------
// �쥤���id���������᥽�å�
//-------------------------------------------------------------
function _Component_ID()
{
	return this._component.id;
}
Component.prototype.id = _Component_ID;

function _Component_FontSize(size)
{
	if(_defined(size))
	{
		this._component.style.fontSize = size + "px";
	}
	else
	{
		return this._component.style.fontSize;
	}
}
Component.prototype.fontSize = _Component_FontSize;


//--------------------------------------------------------------
// ɽ������ɽ���λ��˽�����Ʃ���٤��Ѥ��Ƥ����ֳ֡ʻ��֡ˤ�
// ���ꤹ�롣�ͤ��������ۤ�®���Ѳ����롣
//--------------------------------------------------------------
function _Component_OpacityChangeInterval(interval)
{
	if(typeof(interval) == "undefined")
	{
		return this._opacity_change_interval;
	}
	else
	{
		this._opacity_change_interval = interval;
	}
}
Component.prototype.opacityChangeInterval = _Component_OpacityChangeInterval


//--------------------------------------------------------------
// ������ɽ������HTML���ѹ�����᥽�å�
//--------------------------------------------------------------
function _Component_HTML(html)
{
	var component = this._component;
	
	if(typeof(html) == "undefined")
	{
		return component.innerHTML;
	}
	else
	{
		component.innerHTML = html;
	}
}

Component.prototype.HTML = _Component_HTML;

//----------------------------------------------------------
// �طʿ��ѹ��᥽�å�
//----------------------------------------------------------
function _Component_BackgroundColor(color)
{
	this._component.style.backgroundColor = color;
}
Component.prototype.backgroundColor = _Component_BackgroundColor;


//----------------------------------------------------------
// ��Υܡ������Υ�����������򤹤롣
//----------------------------------------------------------
function _Component_BorderTop(border)
{
	if(_defined(border)){
		var comp = this._component;
		if(MSIE)
		{
			//comp.style.borderTop = border.color();
			//comp.style.border-top-style = border.style();
			//comp.style.border-top-width = border.width();
		}
		else
		{
			comp.style.borderTopColor = border.color();
			comp.style.borderTopStyle = border.style();
			comp.style.borderTopWidth = border.width() + "px";
		}
	}
}
Component.prototype.borderTop = _Component_BorderTop;

//----------------------------------------------------------
// ���Υܡ������Υ�����������򤹤롣
//----------------------------------------------------------
function _Component_BorderBottom(border)
{
	if(_defined(border)){
		var comp = this._component;
		if(MSIE)
		{
		}
		else
		{
			comp.style.borderBottomColor = border.color();
			comp.style.borderBottomStyle = border.style();
			comp.style.borderBottomWidth = border.width() + "px";
		}
	}
}
Component.prototype.borderBottom = _Component_BorderBottom;

//----------------------------------------------------------
// ���Υܡ������Υ�����������򤹤롣
//----------------------------------------------------------
function _Component_BorderLeft(border)
{
	if(_defined(border)){
		var comp = this._component;
		if(MSIE)
		{
		}
		else
		{
			comp.style.borderLeftColor = border.color();
			comp.style.borderLeftStyle = border.style();
			comp.style.borderLeftWidth = border.width() + "px";
		}
	}
}
Component.prototype.borderLeft = _Component_BorderLeft;

//----------------------------------------------------------
// ���Υܡ������Υ�����������򤹤롣
//----------------------------------------------------------
function _Component_BorderRight(border)
{
	if(_defined(border)){
		var comp = this._component;
		if(MSIE)
		{
		}
		else
		{
			comp.style.borderRightColor = border.color();
			comp.style.borderRightStyle = border.style();
			comp.style.borderRightWidth = border.width() + "px";
		}
	}
}
Component.prototype.borderRight = _Component_BorderRight;


//----------------------------------------------------------
// �岼�����Υܡ��������������������ꤹ�롣
// �����θĿ������ꤹ��ս꤬�Ѥ�롣
//
// ����1�ġ��岼����Ʊ������
// ����2�ġ����ꤷ����� "�岼" "����" ������
// ����3�ġ����ꤷ����� "��" "����" "��" ������
// ����4�ġ����ꤷ����� "��" "��" "��" "��" ������
//----------------------------------------------------------
function _Component_Border()
{
	var arg = _Component_Border.arguments;
	
	if(arg.length == 1)
	{
		this.borderTop(arg[0]);
		this.borderBottom(arg[0]);
		this.borderLeft(arg[0]);
		this.borderRight(arg[0]);
		
	}
	else if(arg.length == 2)
	{
		this.borderTop(arg[0]);
		this.borderBottom(arg[0]);
		this.borderLeft(arg[1]);
		this.borderRight(arg[1]);
		
	}else if(arg.length == 3)
	{
		this.borderTop(arg[0]);
		this.borderLeft(arg[1]);
		this.borderRight(arg[1]);
		this.borderBottom(arg[2]);
		
	}
	else if(arg.length == 4)
	{
		this.borderTop(arg[0]);
		this.borderRight(arg[1]);
		this.borderBottom(arg[2]);
		this.borderLeft(arg[3]);
	}
}
Component.prototype.border = _Component_Border;


//----------------------------------------------------------
// X�������κ�ɸ����᥽�å�
// �������Ϥ��ʤ����X�������κ�ɸ���֤���
//----------------------------------------------------------
function _Component_X(x)
{
	var component = this._component;
	
	if(typeof(x) == "undefined")
	{
		var ret = (MSIE) ? component.style.pixelLeft : parseInt(component.style.left);
		return ret;
	}
	else
	{
		if(MSIE)
		{
			component.style.pixelLeft = x;
		}
		else if(Opera)
		{
			component.style.left = x;
		}
		else
		{
			component.style.left = x + "px";
		}
	}
}
Component.prototype.x = _Component_X;


//-------------------------------------------------------------
// Y�������κ�ɸ����᥽�å�
// �������Ϥ��ʤ����Y�������κ�ɸ���֤���
//-------------------------------------------------------------
function _Component_Y(y)
{
	var component = this._component;
	
	if(typeof(y) == "undefined")
	{
		var ret = (MSIE) ? component.style.pixelTop : parseInt(component.style.top);
		return ret;
	}else
	{
		if(MSIE)
		{
			component.style.pixelTop = y;
		}
		else if(Opera)
		{
			component.style.top = y;
		}
		else
		{
			component.style.top = y + "px";
		}
	}
}
Component.prototype.y = _Component_Y;


//-------------------------------------------------------------
// �쥤��ΰ�ư�᥽�å�
// �ʲ�����ˡ�Ȱ�̣��Ʊ����
//
//   var component = new Component(id);
//   component.x(x);
//   component.y(y);
//-------------------------------------------------------------
function _Component_Move(x, y)
{
	this.x(x);
	this.y(y);
}
Component.prototype.move = _Component_Move;


//-------------------------------------------------------------
// �쥤���������᥽�åɡ�
// ��������ꤷ�ʤ���и��ߤ������֤���
//-------------------------------------------------------------
function _Component_Width(width)
{
	var component = this._component;
	
	if(typeof(width) == "undefined")
	{
		var ret = (MSIE) ? component.style.pixelWidth : parseInt(component.style.width);
		return ret;
	}
	else
	{
		if(MSIE)
		{
			component.style.pixelWidth = width;
		}
		else if(Opera)
		{
			component.style.width = width;
		}
		else
		{
			component.style.width = width + "px";
		}
	}
}
Component.prototype.width = _Component_Width;


//-------------------------------------------------------------
// �쥤��ι⤵����᥽�åɡ�
// ��������ꤷ�ʤ���и��ߤι⤵���֤���
//-------------------------------------------------------------
function _Component_Height(height)
{
	var component = this._component;
	
	if(typeof(height) == "undefined")
	{
		var ret = (MSIE) ? component.style.pixelWidth : parseInt(component.style.width);
		return ret;
	}
	else
	{
		if(MSIE)
		{
			component.style.pixelHeight = height;
		}
		else if(Opera)
		{
			component.style.height = height;
		}
		else
		{
			component.style.height = height + "px";
		}
	}
}
Component.prototype.height = _Component_Height;


//-------------------------------------------------------------
// �������ѹ��᥽�åɡ�
// �ʲ���Ʊ����
//
//   var component = new Component(id)
//   component.width(width);
//   component.height(height);
//-------------------------------------------------------------
function _Component_Size(width, height)
{
	this.width(width);
	this.height(height);
}
Component.prototype.size = _Component_Size;


//-------------------------------------------------------------
// �쥤���ɽ������ɽ�����ڤ��ؤ��롣
// ��������ꤷ�ʤ��ä����ϡ����ߤ�ɽ�����֤��֤���
//
// ���� :
//   visible : ɽ������ɽ���λ��� (boolean)
//-------------------------------------------------------------
function _Component_Visible(visible)
{
	var component = this._component;
	
	if(typeof(visible) == "undefined")
	{
		return (component.style.visibility == "visible") ? true : false;
	}
	else
	{
		if(MSIE || Safari || Firefox || Opera)
		{
			if(visible)
			{
				component.style.visibility = "visible";
				this._opacityStep = 10;
				this._opacity = 0;
			}
			else
			{
				this._opacityStep = -10;
				this._opacity = this.opacity();
			}
			
			_addComponent(this);
			
			this.changeOpacity();
		}
		else
		{
			component.style.visibility = (visible) ? "visible" : "hidden";
		}
	}
}
Component.prototype.visible = _Component_Visible;


//-------------------------------------------------------------
// �쥤���Ʃ���٤�������ѹ�����᥽�åɡ�
//-------------------------------------------------------------
function _Component_ChangeOpacity()
{
	var opacity = this._opacity + this._opacityStep;
	
	this.opacity(opacity);
	
	if(opacity >= 100)
	{
		return;
	}
	else if(opacity <= 0)
	{
		this._component.style.visibility = "hidden";
		return
	}
	else
	{
		var interval = this._opacity_change_interval;
		setTimeout("_triggerChangeOpacity('" + this.id() + "')", interval);
	}
}
Component.prototype.changeOpacity = _Component_ChangeOpacity;


//-------------------------------------------------------------
// �쥤���Ʃ���٤���ꤷ���ͤ��ѹ�����᥽�åɡ�
//-------------------------------------------------------------
function _Component_Opacity(opacity)
{
	if(typeof(opacity) == "undefined")
	{
		return this._opacity;
	}
	else
	{
		this._opacity = opacity;
		
		var component = this._component;
		component.style.opacity = opacity / 100;
		component.style.mozOpacity = opacity / 100;
		component.style.filter = "alpha(opacity=" + opacity + ")";
	}
}
Component.prototype.opacity = _Component_Opacity;

//----------------------------------------------------------
// �쥤��򤽤줾���id�򥭡��ˤ�����¸���롣
//----------------------------------------------------------
var _component_list = new Array();

function _addComponent(component)
{
	var id = component.id();
	_component_list[id] = component;
}


//----------------------------------------------------------
// �쥤���Ʃ���٤��ѹ����Ƥ��������ǥ����ޤ���ƤФ��ؿ���
// �����ǻ��ꤵ�줿�쥤���Ʃ�����ѹ��᥽�åɤ򥳡��뤹�롣
//----------------------------------------------------------
function _triggerChangeOpacity(id)
{
	var component = _component_list[id];
	component.changeOpacity();
}


//----------------------------------------------------------
// �������Ϥ��줿�ѿ���������Ѥߤ��ѿ�����Ƚ�ꤹ�롣
//----------------------------------------------------------
function _defined(val)
{
	return (typeof(val) != "undefined") ? true : false;
}



/*==================================================================*/
// �ܡ��������饹�����
// �ǥե���Ȥ������ "1px solid #000000"
/*==================================================================*/
function Border()
{
	this._width = 1;
	this._style = "solid";
	this._color = "#000000";
}


//----------------------------------------------------------
// �ܡ������ο������ꡢ������Ԥ��᥽�åɡ�
//
// var boder = new Border();
// boder.color("#ffffcc");
// alert(boder.color());
//----------------------------------------------------------
function _Border_Color(color)
{
	if(!_defined(color)){
		return this._color;
	}else{
		this._color = color;
	}
}
Border.prototype.color = _Border_Color;


//----------------------------------------------------------
// �ܡ������Υ�����������ꡢ������Ԥ��᥽�åɡ�
// ��������ϰʲ����ͤ����ꤹ�롣
//   none, hidden, solid, double, groove,
//   ridge, inset, outset, dashed, dotted
//
// var boder = new Border();
// boder.style("dashed");
// alert(boder.style());
//----------------------------------------------------------
function _Border_Style(style)
{
	if(!_defined(style)){
		return this._style;
	}else{
		this._style = style;
	}
}
Border.prototype.style = _Border_Style;


//----------------------------------------------------------
// �ܡ��������������ꡢ������Ԥ��᥽�åɡ�
//
// var boder = new Border();
// boder.width(10);
// alert(boder.width());
//----------------------------------------------------------
function _Border_Width(width)
{
	if(!_defined(width)){
		return this._width;
	}else{
		this._width = width;
	}
}
Border.prototype.width = _Border_Width;




/*==================================================================*/
// �֥饦����Υޥ����ΰ��֤���ª���뤿��δؿ���
// �ޥ����ΰ��־�����������ˤϰʲ���2�Ĥδؿ�����Ѥ��롣
//
//   getCurrentMouseX()
//   getCurrentMouseY()
//
/*==================================================================*/
//document.onmousemove = _documentMouseMove;
document.addEventListener('mousemove', _documentMouseMove)

var _mousePosX = 0;
var _mousePosY = 0;

function _documentMouseMove(evt)
{
	_mousePosX = _getEventX(evt);
	_mousePosY = _getEventY(evt);
}

function _getEventX(evt)
{
	return evt.pageX;
/*
	var ret;
	if(Netscape){
		ret = evt.pageX;
	}else if(MSIE || Safari || Chrome){
		ret = event.x + getPageXOffset();
	}else{
		ret = evt.x;
	}

	return ret;
*/
}

function _getEventY(evt)
{
	return evt.pageY;
/*
	var ret;

	if(Netscape){
		ret = evt.pageY;
	}else if(MSIE || Safari || Chrome){
		ret = event.y + getPageYOffset();
	}else{
		ret = event.y;
	}

	return ret;
*/
}

//----------------------------------------------------------
// �֥饦����Υޥ����ݥ��󥿤�X��ɸ���֤���
//----------------------------------------------------------
function getCurrentMouseX()
{
	return _mousePosX;
}

//----------------------------------------------------------
// �֥饦����Υޥ����ݥ��󥿤�Y��ɸ���֤���
//----------------------------------------------------------
function getCurrentMouseY()
{
	return _mousePosY
}


//----------------------------------------------------------
// �������뤵��Ƥ������ɽ�����ϰ��֡�X���ˤ��֤���
//----------------------------------------------------------
function getPageXOffset()
{
	var ret;
	if(Safari || Opera){
		ret = document.body.scrollLeft;
	}else{
		if(document.body.scrollLeft > 0){
			ret = document.body.scrollLeft;
		}else{
			ret = document.documentElement.scrollLeft;
		}
	}

	return ret;
}


//----------------------------------------------------------
// �������뤵��Ƥ������ɽ�����ϰ��֡�Y���ˤ��֤���
//----------------------------------------------------------
function getPageYOffset()
{
	var ret;
	if(Safari || Opera){
		ret = document.body.scrollTop;
	}else{
		if(document.body.scrollTop > 0){
			ret = document.body.scrollTop;
		}else{
			ret = document.documentElement.scrollTop;
		}
	}

	return ret;
}
