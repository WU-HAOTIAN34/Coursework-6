$(function () {

    if (document.getElementById('login') != null) {
        document.getElementById("user").setAttribute("lay-verify", "required")
        document.getElementById("password").setAttribute("lay-verify", "required")
        $(function () {
            layui.use('form', function () {
                var form = layui.form;
            });
        })
        $('input.clear-mem').on("click", function () {
            sessionStorage.clear();
            localStorage.clear();
        })
    }

    if (document.getElementById('user') != null) {
        $.ajax({
            url: '/getSession',
            type: 'POST',
            data: {},
            success: function (data) {
                var user = '' + data[0];
                document.getElementById('user').innerText = 'Welcome: User ' + user;
            }
        })
    }

    if (document.getElementById('province') != null) {
        document.getElementById("province").setAttribute("lay-filter", "province")
        document.getElementById("city").setAttribute("lay-filter", "city")
        layui.use(['form', 'code'], function () {
            form = layui.form;
            layui.code();
            $('#start').xcity();
            $('#end').xcity('广东', '广州市', '东山区');
        });
    }

    $('a.make-order').on("click", function () {
        var item_id = $(this).attr('id');
        var province = $('#province').val();
        var city = $('#city').val();
        var number = $('#number').val();
        a = parseFloat(number)
        b = parseInt(number)
        if (!number) {
            alert('Please enter the number!')
        } else if (a <= 0) {
            alert('The number of item must be larger than 0!')
        } else if (!(a % 1 == 0) && (b % 1 == 0)) {
            alert('Please enter an integer!')
        } else {
            layer.confirm('Are you sure to purchase？', {
                title: "Information",
                btn: ['Pay', 'Cancel'],
                btn1: function (index) {
                    $.ajax({
                        url: '/purchase',
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
                            } else {
                                alert('Purchase failed!')
                            }
                        },
                        error: function () {
                            alert("Error!");
                        }
                    })
                    layer.msg('Payment succeeded, and you can see the order in MY Order!', {
                        icon: 1,
                        time: 1000
                    });
                }
            });
        }
    })

    $('a.make-cart').on("click", function () {
        var item_id = $(this).attr('id');
        item_id = item_id.substring(1);
        var number = $('#number').val();
        var province = $('#province').val();
        var city = $('#city').val();
        a = parseFloat(number)
        b = parseInt(number)
        if (!number) {
            alert('Please enter the number!')
        } else if (a <= 0) {
            alert('The number of item must be larger than 0!')
        } else if (!(a % 1 == 0) && (b % 1 == 0)) {
            alert('Please enter an integer!')
        } else {
            layer.confirm('Are you sure to add to cart？', {
                title: "Information",
                btn: ['Yes', 'Cancel'],
                btn1: function (index) {
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
                            } else {
                                alert('Purchase failed!')
                            }
                        },
                        error: function () {
                            alert("Error!");
                        }
                    })
                    layer.msg('Add ro cart successfully, and you can see it in your shopping cart!', {
                        icon: 1,
                        time: 1000
                    });
                }
            });
        }
    })

    function makeFavor() {
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

    function cancelFavor() {
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

    $('a.refresh-now').on("click", function () {
        $('ul.aim-ul>li').off()
        $("[lay-id='db6d9b451b818ccc9a449383f2f0c450']").on("click", function () {
            document.getElementById('db6d9b451b818ccc9a449383f2f0c450').contentWindow.location.reload(true);
        })
        $("[lay-id='70a17ffa722a3985b86d30b034ad06d7']").on("click", function () {
            document.getElementById('70a17ffa722a3985b86d30b034ad06d7').contentWindow.location.reload(true);
        })
        $("[lay-id='691afc544fc42c0bd32d2b26cb73ca13']").on("click", function () {
            document.getElementById('691afc544fc42c0bd32d2b26cb73ca13').contentWindow.location.reload(true);
        })
    })

    $('.shop-cart').on("click", function () {
        document.getElementById('691afc544fc42c0bd32d2b26cb73ca13').contentWindow.location.reload(true);
    })
    $('.my-favor').on("click", function () {
        document.getElementById('db6d9b451b818ccc9a449383f2f0c450').contentWindow.location.reload(true);
    })
    $('.my-order').on("click", function () {
        document.getElementById('70a17ffa722a3985b86d30b034ad06d7').contentWindow.location.reload(true);
    })

    member_del = function (obj, id) {
        layer.confirm('Are you sure you want to delete？', {
            title: "Information",
            btn: ['Yes', 'No'],
            btn1: function (index) {
                $.ajax({
                    url: '/deleteOrder',
                    type: 'POST',
                    data: {
                        id: id,
                    },
                    dataType: "json",
                    success: function (data) {
                        var judge = parseInt(data.word)
                    },
                    error: function () {
                        alert("Error!");
                    }
                })
                $(obj).parents("tr").remove();
                layer.msg('Delete successfully!', {
                    icon: 1,
                    time: 1000
                });
            }
        });
    }

    delAll = function (argument) {
        layer.confirm('Are you sure you want to delete？', {
            title: "Information",
            btn: ['Yes', 'No'],
            btn1: function (index) {
                var order_list = $(".layui-form-checked").not('.header').parents('tr');
                var length = order_list.length;
                var id_list = ''
                for(var i = 0; i < length; i++){
                    id_list += order_list.eq(i).attr('id') + ' '
                }
                $.ajax({
                    url: '/batchDeleteOrder',
                    type: 'POST',
                    data: {
                        id: id_list,
                    },
                    dataType: "json",
                    success: function (data) {
                        var judge = parseInt(data.word)
                    },
                    error: function () {
                        alert("Error!");
                    }
                })
                $(".layui-form-checked").not('.header').parents('tr').remove();
                layer.msg('Delete successfully!', {
                    icon: 1,
                    time: 1000
                });
            }
        });
    }

    layui.use(
        ['laydate', 'form'],
        function() {
            var laydate = layui.laydate;
            laydate.render({
                elem: '#start'
            });
            laydate.render({
                elem: '#end'
            });
        }
    );

    member_del_item = function (obj, id) {
        layer.confirm('Are you sure you want to delete？', {
            title: "Information",
            btn: ['Yes', 'No'],
            btn1: function (index) {
                $.ajax({
                    url: '/deleteItem',
                    type: 'POST',
                    data: {
                        id: id,
                    },
                    dataType: "json",
                    success: function (data) {
                        var judge = parseInt(data.word)
                    },
                    error: function () {
                        alert("Error!");
                    }
                })
                $(obj).parents("tr").remove();
                layer.msg('Delete successfully!', {
                    icon: 1,
                    time: 1000
                });
            }
        });
    }

    delAll_item = function (argument) {
        layer.confirm('Are you sure you want to delete？', {
            title: "Information",
            btn: ['Yes', 'No'],
            btn1: function (index) {
                var order_list = $(".layui-form-checked").not('.header').parents('tr');
                var length = order_list.length;
                var id_list = ''
                for(var i = 0; i < length; i++){
                    id_list += order_list.eq(i).attr('id') + ' '
                }
                $.ajax({
                    url: '/batchDeleteItem',
                    type: 'POST',
                    data: {
                        id: id_list,
                    },
                    dataType: "json",
                    success: function (data) {
                        var judge = parseInt(data.word)
                    },
                    error: function () {
                        alert("Error!");
                    }
                })
                $(".layui-form-checked").not('.header').parents('tr').remove();
                layer.msg('Delete successfully!', {
                    icon: 1,
                    time: 1000
                });
            }
        });
    }

    if(document.getElementById('description-text')!=null){
        document.getElementById('demo').value=document.getElementById('description-text').placeholder;
        var obj = document.getElementById('description-text');
        obj.remove();
    }

    if(document.getElementById('password-test')!=null){
        document.getElementById('demo').value=document.getElementById('password-test').placeholder;
        var obj = document.getElementById('password-test');
        obj.remove();
    }

    if(document.getElementById('sale-chart')!=null){
        $.ajax({
            url: '/getSale',
            type: 'POST',
            data: {},
            dataType: "json",
            success: function (data) {
                var name = data.name;
                var money_ = data.money;
                var money = new Array(money_.length)
                for(var i=0; i <money_.length;i++){
                    money[i] = parseInt(money_[i])
                }
                var dom = document.getElementById('container');
                var myChart = echarts.init(dom, null, {
                    renderer: 'canvas',
                    useDirtyRect: false
                });
                var app = {};
                var option;
                option = {
                    title: {
                        text: 'Total Sales for Each Item'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: name
                    },
                    series: [{
                        name: '2011',
                        type: 'bar',
                        data: money
                    }]
                };
                if (option && typeof option === 'object') {
                    myChart.setOption(option);
                }
                window.addEventListener('resize', myChart.resize);
            }
        })
    }

    $('a#register-button').on("click", function () {
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm = $('#confirm').val();
        var name = $('#name').val();
        var phone = $('#phone').val();
        var identity = $('#identity').val();
        if (username == '' || password == '' || confirm == '' || name =='' || phone == '') {
            alert('Please enter all the required items!');
        } else if (username.length>50 || name.length>50) {
            alert('Username and name should be less than 50 characters!');
        } else if (password.length <= 6) {
            alert('The password should be longer than 6 characters!');
        } else if (password != confirm) {
            alert('The passwords entered twice are different!');
        } else {
            $.ajax({
                url: '/registerVali',
                type: 'POST',
                data: {
                    username: username,
                    password: password,
                    name: name,
                    phone: phone,
                    identity: identity
                },
                dataType: "json",
                success: function (data) {
                    var a = parseInt(data.word);
                    if (a == 0) {
                        alert('The username already exists!');
                    } else {
                        alert('Register successfully!');
                        window.location = '/';
                    }
                },
                error: function () {
                    alert("Error!");
                }
            })
        }
    })

    $('input#login-button').on("click", function () {
        var username = $('#user').val();
        var password = $('#password').val();
        var identity = $('#identity').val();
        if (username == '' || password == '') {
            alert('Please enter all the required items!');
        } else {
            $.ajax({
                url: '/loginVali',
                type: 'POST',
                data: {
                    username: username,
                    password: password,
                    identity: identity
                },
                dataType: "json",
                success: function (data) {
                    var a = parseInt(data.word);
                    if (a == 0) {
                        alert('Username or password error!');
                    } else if(a == 1){
                        alert('Login successfully!');
                        window.location = '/user';
                    }else if(a == 2){
                        alert('Login successfully!');
                        window.location = '/admin';
                    }
                },
                error: function () {
                    alert("Error!");
                }
            })
        }
    })


})

