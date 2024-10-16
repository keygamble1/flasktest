
const recommend_elements=document.getElementsByClassName("recommend");
Array.from(recommend_elements).forEach(function(element){
    element.addEventListener('click',function(){
        if(confirm('정말추천?')){
            location.href=this.dataset.uri
        }

    });
});
const page_elements=document.getElementsByClassName("page-link");
Array.from(page_elements).forEach(function(element){
    element.addEventListener('click',function(){
        document.getElementById('page').value=this.dataset.page;
        document.getElementById('searchForm').onsubmit()
    });
});

const btn_search=document.getElementById("btn_search");
Array.from(btn_search).forEach(function(element){
    element.addEventListener('click',function(){
        document.getElementById('kw').value=document.getElementById('search_kw').value
        
    });
});