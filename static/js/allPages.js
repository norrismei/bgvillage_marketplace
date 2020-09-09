"use strict";

function showMeeple() {
    $('.meeple').hide();
    $(this).children('.meeple').show();
}

function hideMeeple() {
    $(this).children('.meeple').hide();
}

function toggleMeeple() {
    $('.nav-link').hover(showMeeple, hideMeeple);
}

function resetMeeple() {
    $('.meeple').removeAttr('style')
}

$('.navbar-nav').hover(toggleMeeple, resetMeeple)