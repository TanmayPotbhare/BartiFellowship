$(document).ready(function () {
    trtimail = $('.trti-mail').css('font-size');
    mobnumber = $('.mob-no').css('font-size');
    headerAnchor = $('.header-menu').css('font-size');
    fellowshipText = $('.fellowship-text').css('font-size');
    font13 = $('.font-13').css('font-size');
    navlink = $('.navigation').css('font-size');
    bannertext = $('.bannertext').css('font-size');
    span_h3 = $('.h3').css('font-size');
    banner_title = $('.banner-title').css('font-size');
    criteria_heading=  $('.elig').css('font-size');
    esteps_1 = $('h3.esteps-1').css('font-size');
    esteps_2= $('.esteps-2').css('font-size');
    sectionheading = $('.sectionheading').css('font-size');
    faq_question = $('.accordion-header1').css('font-size');
    faq_answer1 = $('#faq-content-2').css('font-size');
    faq_answer2 = $('#faq-content-3').css('font-size');
    footer_header=  $('.footer-header').css('font-size');
    footerlink = $('.footer-link').css('font-size');
    footer_subtitle= $('.footer-subtitle').css('font-size');
    copyright = $('.copyrightlink').css('font-size');
    contact_home =  $('.contact-home').css('font-size');
    contact_us =  $('.contact-us').css('font-size');
    contact_button =  $('.getstarted').css('font-size');
    contact_page_info = $('.contact-page-info').css('font-size');
    contact_page_info_content = $('.contact-page-info-content').css('font-size');
    year_report = $('.year-report').css('font-size');
    // mailustitle = $('#mail-us-title').css('font-size');
    // mailus = $('#mailus').css('font-size');
    
    
    // calltitle = $('.call-title').css('font-size');
    // callnumber = $('.call-number').css('font-size');
    
    
    // bannertext2 = $('#bannertext2').css('font-size');
    // recentupdates = $('.recentupdates').css('font-size');
    // importantnews = $('.importantnews').css('font-size');
    // accordionmaintext = $('.accordion-main-text').css('font-size');
    // accordionsubtext = $('.accordion-subtext').css('font-size');
    // 
    // greenlink = $('.green-link').css('font-size');
    // bluelink = $('.blue-link').css('font-size');
    // activity = $('.activity').css('font-size');
    // seemore = $('.seemore').css('font-size');
    // program = $('.program').css('font-size');
    // affairs = $('.affairs').css('font-size');
    // announcement = $('.announcement').css('font-size');
    // gallerysectionname = $('.gallerysectionname').css('font-size');
    // footerheadtxt = $('.footer-head-txt').css('font-size');
    // footerlink = $('.footer-link').css('font-size');
    // textright = $('.textright').css('font-size');
    // copyright = $('.copyrightlink').css('font-size');
    // resizingp = $('.resizingp').css('font-size');
    // dhfontSize = $('h2[data-type="component-text"]').css('font-size');
    // dpfontSize = $('p[data-type="component-text"]').css('font-size');
    // dolfontSize = $('ol[data-type="component-text"]').css('font-size');
    // h4size = $('h4.text-white.font-weight-bold').css('font-size');
    // sidebar = $('#main-content').css('font-size');
    // fontheading = $('.font-heading').css('font-size');
    // h4title = $('h4.title').css('font-size');
    // navmenulink = $('a.nav-link').css('font-size');
    // team_member_header = $('.emp_wrapper .h5').css('font-size');
    // emp_details = $('.emp_details').css('font-size');
    loop = 0
}
);

function fontIncrease() {
    var menu_link_size = parseInt($('.navbar-nav .nav-link').css('font-size')) + 1;
    if (loop <= 5) {
        $('.font-14').css('font-size', parseInt($('.font-14').css('font-size')) + 1 );
        $('.font-13').css('font-size', parseInt($('.font-13').css('font-size')) + 1 );
        $('.header-menu').css('font-size', parseInt($('.header-menu').css('font-size')) + 1);
        $('.fellowship-text').css('font-size', parseInt($('.fellowship-text').css('font-size')) + 1);
        $('.navigation').css('font-size', parseInt($('.navigation').css('font-size')) + 1);
        $('.bannertext').css('font-size', parseInt($('.bannertext').css('font-size')) + 1);
        $('.h3').css('font-size', parseInt($('.h3').css('font-size')) + 1);                               
        $('.banner-title').css('font-size', parseInt($('.banner-title').css('font-size')) + 1);
        $('.elig').css('font-size', parseInt($('.elig').css('font-size')) + 1);
        $('h3.esteps-1').css('font-size', (parseInt($('h3.esteps-1').css('font-size')) + 1));
        $('.esteps-2').css('font-size', parseInt($('.esteps-2').css('font-size')) + 1);
        $('.sectionheading').css('font-size', parseInt($('.esteps-2').css('font-size')) + 1);
        $('.accordion-header1').css('font-size', parseInt($('.accordion-header1').css('font-size')) + 1);
        $('#faq-content-2').css('font-size', parseInt($('#faq-content-2').css('font-size')) + 1);
        $('#faq-content-3').css('font-size', parseInt($('#faq-content-3').css('font-size')) + 1);
        $('.footer-header').css('font-size', parseInt($('.footer-header').css('font-size')) + 1);
        $('.footer-link').css('font-size', parseInt($('.footer-link').css('font-size')) + 1);
        $('.footer-subtitle').css('font-size', parseInt($('.footer-link').css('font-size')) + 1);
        $('.copyrightlink').css('font-size', parseInt($('.copyrightlink').css('font-size')) + 1);
        $('.contact-home').css('font-size', parseInt($('.contact-home').css('font-size')) + 1);
        $('.contact-us').css('font-size', parseInt($('.contact-us').css('font-size')) + 1);
        $('.getstarted').css('font-size', parseInt($('.getstarted').css('font-size')) + 1);
        $('.contact-page-info').css('font-size', parseInt($('.contact-page-info').css('font-size')) + 1);
        $('.contact-page-info-content').css('font-size', parseInt($('.contact-page-info').css('font-size')) + 1);
        $('.year-report').css('font-size', parseInt($('.year-report').css('font-size')) + 1);
        // $('#mail-us-title').css('font-size', parseInt($('#mail-us-title').css('font-size')) + 1);
        // $('#mailus').css('font-size', parseInt($('#mailus').css('font-size')) +   1);
        
        
        // $('.call-title').css('font-size', parseInt($('.call-title').css('font-size')) + 1);
        // $('.call-number').css('font-size', parseInt($('.call-number').css('font-size')) + 1);
       
        
        // $('#bannertext2').css('cssText', 'font-size: ' + (parseInt($('#bannertext2').css('font    -size')) + 1) + 'px !important');
        // $('.recentupdates').css('cssText', 'font-size: ' + (parseInt($('.recentupdates').css('font-size')) + 1) + 'px !important');
        // $('.importantnews').css('cssText', 'font-size: ' + (parseInt($('.importantnews').css('font-size')) + 1) + 'px !important');
        // $('.accordion-main-text').css('cssText', 'font-size: ' + (parseInt($('.accordion-main-text').css('font-size')) + 1) + 'px !important;');
        // $('.accordion-subtext').css('cssText', 'font-size: ' + (parseInt($('.accordion-subtext').css('font-size')) + 1) + 'px !important;');
        // $('.sectionheading').css('cssText', 'font-size: ' + (parseInt($('.sectionheading').css('font-size')) + 1) + 'px !important;');
        // $('.green-link').css('cssText', 'font-size: ' + (parseInt($('.green-link').css('font-size')) + 1) + 'px !important;');
        // $('.blue-link').css('cssText', 'font-size: ' + (parseInt($('.blue-link').css('font-size')) + 1) + 'px !important;');
        // $('.activity').css('cssText', 'font-size: ' + (parseInt($('.activity').css('font-size')) + 1) + 'px !important;');
        // $('.seemore').css('cssText', 'font-size: ' + (parseInt($('.seemore').css('font-size')) + 1) + 'px !important;');
        // $('.program').css('cssText', 'font-size: ' + (parseInt($('.program').css('font-size')) + 1) + 'px !important;');
        // $('.affairs').css('cssText', 'font-size: ' + (parseInt($('.affairs').css('font-size')) + 1) + 'px !important;');
        // $('.announcement').css('cssText', 'font-size: ' + (parseInt($('.announcement').css('font-size')) + 1) + 'px !important;');
        // $('.gallerysectionname').css('cssText', 'font-size: ' + (parseInt($('.gallerysectionname').css('font-size')) + 1) + 'px !important;');
        // $('.footer-head-txt').css('cssText', 'font-size: ' + (parseInt($('.footer-head-txt').css('font-size')) + 1) + 'px !important;');
        // $('.footer-link').css('cssText', 'font-size: ' + (parseInt($('.footer-link').css('font-size')) + 1) + 'px !important;');
        // $('.textright').css('cssText', 'font-size: ' + (parseInt($('.textright').css('font-size')) + 1) + 'px !important;');
        // $('.copyrightlink').css('cssText', 'font-size: ' + (parseInt($('.copyrightlink').css('font-size')) + 1) + 'px !important;');
        // $('#main-content').css('cssText', 'font-size: ' + (parseInt($('#main-content').css('font-size')) + 1) + 'px !important;');
        // $('.font-heading').css('cssText', 'font-size: ' + (parseInt($('.font-heading').css('font-size')) + 1) + 'px !important;');
        // $('.resizingp').css('cssText', 'font-size: ' + (parseInt($('.resizingp').css('font-size')) + 1) + 'px !important;');
        // $('h2[data-type="component-text"]').css('cssText', 'font-size: ' + (parseInt($('h2[data-type="component-text"]').css('font-size')) + 1) + 'px !important; ');
        // $('p[data-type="component-text"]').css('cssText', 'font-size: ' + (parseInt($('p[data-type="component-text"]').css('font-size')) + 1) + 'px !important;');
        // $('ol[data-type="component-text"]').css('cssText', 'font-size: ' + (parseInt($('ol[data-type="component-text"]').css('font-size')) + 1) + 'px !important;');
        // $('h4.text-white.font-weight-bold').css('cssText', 'font-size: ' + (parseInt($('h4.text-white.font-weight-bold').css('font-size')) + 1) + 'px !important;');
        // $('h4.title').css('cssText', 'font-size: ' + (parseInt($('h4.title').css('font-size')) + 1) + 'px !important;');
        // $('.emp_details').css('cssText', 'font-size: ' + (parseInt($('.emp_details').css('font-size')) + 1) + 'px !important;');
        // $('.emp_wrapper .h5').css('cssText', 'font-size: ' + (parseInt($('.emp_wrapper .h5').css('font-size')) + 1) + 'px !important;');
        // $('.navbar-nav .nav-link').css('cssText', 'font-size: ' + menu_link_size + 'px !important;');
        loop = loop + 1
    }
}