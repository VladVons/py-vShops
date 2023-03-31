$$.ready(()=>{
  $$.load('/default/css/styles.css')
  $$.load('/default/css/desktop.css', function(){
    console.log('desktop.css loaded')
  })
})