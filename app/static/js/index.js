$(function (){

    if(document.getElementById('login')!=null){
        document.getElementById("user").setAttribute("lay-verify", "required")
        document.getElementById("password").setAttribute("lay-verify", "required")
         $(function  () {
            layui.use('form', function(){
              var form = layui.form;
            });
        })
    }

    if(document.getElementById('user')!=null){
        $.ajax({
            url: '/getSession',
            type: 'POST',
            data: {},
            success: function (data) {
                var user = '' + data[3];
                document.getElementById('user').innerText= 'Welcome: ' + user;
            }
        })
    }

    if(document.getElementById('province')!=null){
        document.getElementById("province").setAttribute("lay-filter", "province")
        document.getElementById("city").setAttribute("lay-filter", "city")
        layui.use(['form','code'], function(){
            form = layui.form;
            layui.code();
            $('#start').xcity();
            $('#end').xcity('广东','广州市','东山区');
          });
    }

    $('a.make-order').on("click", function() {
        var item_id = $(this).attr('id');
        var province = $('#province').val();
        var city = $('#city').val();
        var number = $('#number').val();
        a = parseFloat(number)
        b = parseInt(number)
        if (!number){
            alert('Please enter the number!')
        }else if (a<=0){
            alert('The number of item must be larger than 0!')
        }else if (!(a%1==0)&&(b%1==0)){
            alert('Please enter an integer!')
        }else{
            $.ajax({
                url: '/purchase',
                type: 'POST',
                data: {
                    item_id: item_id,
                    province: province,
                    city: city,
                    number: number
                },
                dataType:"json",
                success: function (data) {
                    var judge = parseInt(data.word)
                    if(judge==1){
                        alert('You have successfully purchased!')
                    }else{
                        alert('Purchase failed!')
                    }
                },
                error:function (){
                    alert("Error!");
                }
            })
        }
    })

     $('a.make-cart').on("click", function() {
        var item_id = $(this).attr('id');
        item_id = item_id.substring(1);
        var number = $('#number').val();
        var province = $('#province').val();
        var city = $('#city').val();
        a = parseFloat(number)
        b = parseInt(number)
        if (!number){
            alert('Please enter the number!')
        }else if (a<=0){
            alert('The number of item must be larger than 0!')
        }else if (!(a%1==0)&&(b%1==0)){
            alert('Please enter an integer!')
        }else {
            $.ajax({
                url: '/collect',
                type: 'POST',
                data: {
                    item_id: item_id,
                    province: province,
                    city: city,
                    number: number
                },
                dataType: "json",
                success: function (data) {
                    var judge = parseInt(data.word)
                    if (judge == 1) {
                        alert('Has been added to the shopping cart!')
                    } else {
                        alert('Purchase failed!')
                    }
                },
                error: function () {
                    alert("Error!");
                }
            })
        }
    })

    function makeFavor(){
        var item_id = $(this).attr('id');
        document.getElementById(item_id).setAttribute("class", "layui-btn layui-btn-danger layui-col-lg6 layui-col-md6 layui-col-sm6 layui-col-xs6 cancel-favor");
        document.getElementById(item_id).innerHTML = "<i class=\"iconfont\">&#xe7ce;</i> Favor"
        $.ajax({
            url: '/makeFavor',
            type: 'POST',
            data: {
                item_id: item_id,
            },
            dataType: "json",
            success: function (data) {
                var judge = parseInt(data.word)
                if (judge == 1) {
                    var t=setTimeout("alert('Collect successfully!')",300)
                } else {
                    alert('Collection failed!')
                }
            },
            error: function () {
                alert("Error!");
            }
        })
        $(this).off();
        $(this).on("click", cancelFavor);
    }

    function cancelFavor(){
        var item_id = $(this).attr('id');
        document.getElementById(item_id).setAttribute("class", "layui-btn layui-btn-normal layui-col-lg6 layui-col-md6 layui-col-sm6 layui-col-xs6 make-favor");
        document.getElementById(item_id).innerHTML = "<i class=\"iconfont\">&#xe7ce;</i> Normal"
        $.ajax({
            url: '/cancelFavor',
            type: 'POST',
            data: {
                item_id: item_id,
            },
            dataType: "json",
            success: function (data) {
                var judge = parseInt(data.word)
                if (judge == 1) {
                    var t=setTimeout("alert('Cancel successfully!')",300)
                } else {
                    alert('Cancel failed!')
                }
            },
            error: function () {
                alert("Error!");
            }
        })
        $(this).off();
        $(this).on("click", makeFavor);
    }

    $('a.make-favor').on("click", makeFavor)

    $('a.cancel-favor').on("click", cancelFavor)

})

