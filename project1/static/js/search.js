document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('form').onsubmit = () => {
        var Ourreq = new XMLHttpRequest();
        var filter = document.getElementById('filter').value;
        var search = document.getElementById('search').value;
        Ourreq.open('POST', '/api/search');
        Ourreq.onload = () => {
            var ourData = JSON.parse(Ourreq.responseText);
            if (ourData.success) {
                if (ourData.results.length > 0) {
                    var htmlString = "";
                    var counter = 1
                    ourData.results.forEach(sta => {
                        htmlString += "<tr> <td>" + counter + "</td> <td>" + sta["title"] + "</td><td><a href='/book/isbn=" + sta["ISBN"] + "'>" + sta["ISBN"] + "</a> </td> </tr>";
                        counter++;
                    });
                    document.getElementById("results-info").innerHTML = htmlString
                }
            }
        }
        Ourreq.send(JSON.stringify({ "filter": filter, "search": search }));
        return false;
    }
});