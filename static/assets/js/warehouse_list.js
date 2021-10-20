var send_data = {}

$(document).ready(function () {
     getWarehouse();

     $('.warehouse_name').on('change', function () {
        console.log("On Warehouse selected")
        send_data['warehouse_name'] = this.value
        console.log(this.value)
    });



    // Close LC Button Clicked
    $("#closed_lc_id").click(function(){
       console.log("Closed LC Button Clicked ")
       sendWarehouseName()
     })

})

function getWarehouse() {
        console.log("getWarehouse Called")
        let url = $(".warehouse_name").attr("url");
        $.ajax({
            method: 'GET',
            url: url,
            data: {},
            success: function (result) {
                console.log(result)
                countries_option = "<option value='all' selected>Select....</option>";
                $.each(result, function (a, b) {
                    countries_option += "<option value="+b.id+">" + b.warehouse_name + "</option>"
                });
                $(".warehouse_name").html(countries_option)
            },
            error: function(response){
                console.log(response)
            }
        });
    }


function sendWarehouseName() {
        console.log("getWarehouse Called")
        let url = $(".warehouse_name").attr("url");
        $.ajax({
            method: 'GET',
            url: url,
            data: {},
            success: function (result) {
                console.log(result)
                countries_option = "<option value='all' selected>Select....</option>";
                $.each(result, function (a, b) {
                    countries_option += "<option value="+b.id+">" + b.warehouse_name + "</option>"
                });
                $(".warehouse_name").html(countries_option)
            },
            error: function(response){
                console.log(response)
            }
        });
    }


