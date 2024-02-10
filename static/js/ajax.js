$(document).ready( function(){
    fetchAll();
});
var Datajsons = [];
var oldalpha;
function fetchAll(){
    $.ajax({ 
        type: 'GET', 
        url: 'http://127.0.0.1:8080/documents', 
        dataType: 'json',
        success: function (data) { 
            var items = []
            $.each( data, function( key, val ) {
                $.each(this, function(j, jsonData){
                    var image = new Image();
                    image.src = jsonData.pict;
                    items.push( 
                        "<tr id='row"+ jsonData.key +"'>" + 
                            "<td>" + (j) + "</td><td>" + 
                            jsonData.doctype + "</td><td>" + 
                            jsonData.country + "</td><td>" +
                            jsonData.mrz  + "</td><td>" +
                            jsonData.alphahash + "</td><td>" + 
                            '<img id=img'+ JSON.stringify(j)+ ' src="' + jsonData.picture + '"></td><td>' +
                            jsonData.dpsscore + "</td><td>" + 
                            '<button type="submit" class="col-md-5 btn btn-outline-danger" value="'+ jsonData.key +'"' + 'onclick=delitem('+         JSON.stringify(jsonData.key)+ ')>delete</button>' +
                            '<button class="col-md-5 edit-button btn btn-outline-warning" data-value="'+ JSON.stringify(j) +'">edit</button>' + 
                            '<button class="col-md-5 rescore btn btn-outline-default" data-value="'+ JSON.stringify(j) +'">rescore</button>' +
                        "</tr>" 
                        );
                });
                $(items.join("")).appendTo(".display");
            });
            // Datajsons = data.Items;
            // console.log(Datajsons);
            $("#tdatas").load(location.href + " #tdatas");
        }
    });
};

$('#tdatas').on('click', 'button.edit-button', function() {
    var list = [];
    var $row = $(this).closest("tr"); 
    var $tds = $row.find("td");
    
    $.each($tds, function() {
        list.push($(this).text());
        console.log(this);
    });  

    oldalpha = list[4];
    $("#docstype").val(list[1]);
    $("#country").val(list[2]);
    $("#mrz").val(list[3]);
    $("#alphahash").val(list[4]);
    $("#imginput").val(list[5]);

    $('#name').attr('readonly', false);
    $('.crbtn').attr('hidden', true);
    $('.upbtn').attr('hidden', false);
    
});

$(".upbtn").click(function(){
    var doctypes = $("#docstype").val();
    var countrys = $("#country").val();
    var mrzs = $("#mrz").val();
    var alphahashs = $("#alphahash").val();

    var $img = $tds.find("img").attr("src");
    console.log($img);
    var picts = $img;
    // var dpsscores = $("#dpsscore").val();
    var dpsscores = 23;
    console.log(doctypes, countrys, mrzs, alphahashs, dpsscores);
    var mydata = {
            doctype     : doctypes,
            country     : countrys,
            mrz         : mrzs,
            alphahash   : alphahashs,
            picture     : picts,
            dpsscore    : parseInt(dpsscores), 
        }
    var dataJSON = JSON.stringify(mydata);
    console.log(dataJSON);
    $.ajax({
        type: 'PUT',
        url: 'http://127.0.0.1:8080/documents/'+String(oldalpha),
        dataType: 'json',
        contentType: "application/json",
        data: dataJSON,
        success: function(){
            alert("Data Updated");
            fetchAll();
            $('#name').attr('readonly', false);
            $('.upbtn').attr('hidden', false);
            location.reload(true);
        }
    });
});

function delitem(key){
    var responseDel = confirm("Delete this?");
    if (responseDel == true) {
        $.ajax({
            type: 'DELETE',
            url: 'http://127.0.0.1:8080/documents/'+ key,
            dataType: 'json',
            success: function(respdelete){
                console.log(respdelete);
                $("#row"+key).remove();
            }
        });
    } else {
        return null;
    }
    
};

function createitem(){
    var doctypes = $("#docstype").val();
    var countrys = $("#country").val();
    var mrzs = $("#mrz").val();
    var alphahashs = $("#alphahash").val();
    var picts = $("#imgb64").html();
    // var dpsscores = $("#dpsscore").val();
    var dpsscores = 23;
    console.log(doctypes, countrys, mrzs, alphahashs, dpsscores);
    var mydata = {
            doctype     : doctypes,
            country     : countrys,
            mrz         : mrzs,
            alphahash   : alphahashs,
            picture     : picts,
            dpsscore    : parseInt(dpsscores), 
        }
    var dataJSON = JSON.stringify(mydata);
    console.log(dataJSON);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8080/documents',
        dataType: 'json',
        contentType: "application/json",
        data: dataJSON,
        success: function(data){
            console.log(data.data);
            alert("Data createrd");
        }
    });
}

$('.crbtn').click(function() {
    createitem();
});

$('#tdatas').on('click', 'button.rescore', function() {
    list = []
    var $row = $(this).closest("tr"); 
    var $tds = $row.find("td");
    $.each($tds, function() {
        list.push($(this).text());
    }); 
    console.log(list[4]); 
    alpha = list[4];
    $.ajax({
        type: 'PUT',
        url: 'http://127.0.0.1:8080/dpsrenew/'+alpha,
        dataType: 'json',
        contentType: "application/json",
        success: function(){
            alert("DPS renew");
            fetchAll();
            location.reload(true);
        }
    });
    
});

