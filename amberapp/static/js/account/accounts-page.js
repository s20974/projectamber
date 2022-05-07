
function showHidden (objName) {
if ( $(objName).css('display') == 'none' ) {
$(objName).animate({height: 'show'}, 600);
} else {
$(objName).animate({height: 'hide'}, 500);
}
};