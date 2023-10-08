var mainpH= document.getElementById('main');
document.querySelectorAll('button').forEach(function(e){
    e.addEventListener('click', function(){
        mainpH.classList.toggle('open');
    })
})
