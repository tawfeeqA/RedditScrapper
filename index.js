function output(arr){

}
document.getElementById('submit').onclick = function(){
    console.log('aaa');
    subreddit= document.getElementById('subred').value;
    nPosts= document.getElementById('numposts').value;
    posttype=document.getElementById('posttype').value;
    sTerms= document.getElementById('terms').value;
    console.log([subreddit,nPosts,posttype,sTerms]);
    output([subreddit,nPosts,posttype,sTerms]);
}
