import Cookies from 'js-cookie';
const setCookie = (data)=> {
    if(!Cookies.get('bigsyncData')){
        Cookies.set('bigsyncData',data);
    }
    else{
        let temp = Cookies.get('bigsyncData');
        temp = temp.split(',')
        console.log(temp)
        data.forEach((d)=>{
            temp.push(d)
        })
        Cookies.set('bigsyncData', temp);
    }
  }
export default setCookie  
