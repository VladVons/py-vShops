$$.ready(()=>{
  $$.load('/default/css/styles.css')
  $$.load('/default/css/desktop.css', function(){
    $$('body').css({opacity: 1, transition: 'opacity .5s ease'})
  })
})