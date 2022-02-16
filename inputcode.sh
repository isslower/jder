mobile=$1
rm -rf ${mobile}pt
appid=959
qversion=1.0.0
country_code=86
smscode=$2

pt(){
appid=959
qversion=1.0.0
country_code=86
ts=$(expr $(date +%s%N) / 1000000)
sub_cmd=3
gsalt=$(cat ${mobile}ck | grep -o "gsalt.*" | cut -d '"' -f3)
guid=$(cat ${mobile}ck | grep -o "guid.*" | cut -d '"' -f3)
lsid=$(cat ${mobile}ck | grep -o "lsid.*" | cut -d '"' -f3)
rsa_modulus=$(cat ${mobile}ck | grep -o "rsa_modulus.*" | cut -d '"' -f3)
ck=$(echo "guid=$guid;  lsid=$lsid;  gsalt=$gsalt;  rsa_modulus=$rsa_modulus;")
gsign=$(echo -n $appid$qversion$ts"36"$sub_cmd$gsalt | md5sum | cut -d ' ' -f1)
d="country_code=$country_code&client_ver=1.0.0&gsign=$gsign&smscode=$smscode&appid=$appid&mobile=$mobile&cmd=36&sub_cmd=$sub_cmd&qversion=$qversion&ts=$ts"
l=${#d}
curl -s -k -i --raw -o ${mobile}pt --http2 -X POST -H "Host:qapplogin.m.jd.com" -H "cookie:$ck" -H "user-agent:Mozilla/5.0 (Linux; Android 10; V1838T Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.87 Mobile Safari/537.36 hap/1.9/vivo com.vivo.hybrid/1.9.6.302 com.jd.crplandroidhap/1.0.3 ({"packageName":"com.vivo.hybrid","type":"deeplink","extra":{}})" -H "accept-language:zh-CN,zh;q=0.9,en;q=0.8" -H "content-type:application/x-www-form-urlencoded; charset=utf-8" -H "content-length:$l" -H "accept-encoding:" -d "country_code=$country_code&client_ver=1.0.0&gsign=$gsign&smscode=$smscode&appid=$appid&mobile=$mobile&cmd=36&sub_cmd=$sub_cmd&qversion=$qversion&ts=$ts" "https://qapplogin.m.jd.com/cgi-bin/qapp/quick"
err_msg=$(cat ${mobile}pt | grep -o "err_msg.*" | cut -d '"' -f3)
if [ -z $err_msg ]
then pt_key=$(cat ${mobile}pt | grep -o "pt_key.*" | cut -d '"' -f3)
pt_pin=$(cat ${mobile}pt | grep -o "pt_pin.*" | cut -d '"' -f3)
qlck="pt_key=$pt_key;pt_pin=$pt_pin;"
echo ${mobile}:$qlck
echo $qlck > ${mobile}qlck
rm -rf ${mobile}ck ${mobile}sc ${mobile}pt
else echo $err_msg
fi
}
pt