$(document).ready(function(){
    
    $('.close_menu').on('click', function(){
        
        setTimeout(()=>{
            $('.mobile_menu').addClass('opacity-0')
            $('.mobile_menu').addClass('invisible')
            $('.mobile_menu_container').addClass('-translate-x-full')
        }, 300)
    })
    $('.open_menu').on('click', function(){
        
        $('.mobile_menu').removeClass('invisible')
        setTimeout(()=>{
            $('.mobile_menu').removeClass('opacity-0')
            $('.mobile_menu_container').removeClass('-translate-x-full')
        }, 300)
    })

})