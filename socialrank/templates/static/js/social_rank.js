
var COUNT_INTERVAL = 30;
var count=COUNT_INTERVAL;
var counter=setInterval(timer, 1000); // 1 second
var LINK_DELIM = "&$$";

function timer() {
  count = count-1;
  if (count <= 0) {
     clearInterval(counter);
     refresh_links();
     count = COUNT_INTERVAL;
     counter=setInterval(timer, 1000);
  }
  document.getElementById("timer").innerHTML=count + "";
}

function refresh_links() {
   $.post('/refresh_links/', { status:"True" },
      function(response) {
           links = response['data'];
           link_vals = [];
           for (var i=0; i<links.length; i++) {
                link_vals.push(links[i]["links"]);
           }

           var loc = $("#listing-container");
           //loc.empty();
           var html = "";

           for (var j=0; j < link_vals.length; j++) {

                  var url = link_vals[j].split(LINK_DELIM)[0];
                  var title = link_vals[j].split(LINK_DELIM)[1];
                  var img = link_vals[j].split(LINK_DELIM)[2];
                  var age = link_vals[j].split(LINK_DELIM)[3];
                  var status = link_vals[j].split(LINK_DELIM)[4];
                  var shares = link_vals[j].split(LINK_DELIM)[5];

                  html += format_listing(url, title,
                          img, age, status, shares);
                  /*
                  loc.append(
                      format_listing(url, title,
                          img, age, status, shares)
                  );*/
             }
          loc.html(html).fadeIn(3000);
      }, 'json'
   );
}

function format_listing(url, title, img, age, status, shares) {
      var statusHtml = '';

      if (age == null) {
          age = "";
      }
      if (status == 'POSITIVE') {
         statusHtml = '<span style="color:green;">▲</span>';
      }
      else if (status == 'NEGATIVE') {
          statusHtml = '<span style="color:red;">▼</span>';
      }
      else {
          statusHtml = '<span style="color:gray;">--</span>';
      }

      return '<div style="height: 65px;">'+
                '<div class="row">'+
                    '<div class="col-md-1" style="text-align: center;">'+
                        statusHtml +
                    '</div>'+
                    '<div class="col-md-1">'+
                        '<img class="thumb" src="'+ img + '">' +
                    '</div>'+
                    '<div class="col-md-10">'+
                        '<p class="lead"><a target="_blank" href="'+ url +'">'+
                           title + '</a></p>'+
                        '<p class="small"> published ' +
                            age + ' ago, ' + 'shared ' +
                            shares + ' times' +
                        '</p>' +
                    '</div>'+
                '</div>'+
             '</div>';
}

$(document).ready(function() {
    $("img").error(function () {
        $(this).hide();
    });
});