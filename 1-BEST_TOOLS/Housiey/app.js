var hinjewadiDevlopers = require('./hinjewadi.json');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
    path: './hinjewadifile.csv',
    header: [
        {id: 'project_name', title: 'Name'},
        {id: 'overall_price_range', title: 'Range'},
        { id: 'rera_possession', title: 'Possetion' },
        { id: 'location', title: 'location' },
        { id: 'config0', title: 'c0' },
        { id: 'area0', title: 'a0' },
        { id: 'price0', title: 'p0' },

        { id: 'config1', title: 'c1' },
        { id: 'area1', title: 'a1' },
        { id: 'price1', title: 'p1' },

        { id: 'config2', title: 'c2' },
        { id: 'area2', title: 'a2' },
        { id: 'price2', title: 'p2' },

        { id: 'config3', title: 'c3' },
        { id: 'area3', title: 'a3' },
        { id: 'price3', title: 'p3' },

        { id: 'config4', title: 'c4' },
        { id: 'area4', title: 'a4' },
        { id: 'price4', title: 'p4' },

        { id: 'config5', title: 'c5' },
        { id: 'area5', title: 'a5' },
        { id: 'price5', title: 'p5' }
    ]
});
 

var projcts = hinjewadiDevlopers["projects"]
var finalResult = []
for (let index = 0; index < projcts.length; index++) {
    const e = projcts[index];
    var obj = {};
    obj["project_name"] = projcts[index]["project_name"];
    obj["overall_price_range"] = projcts[index]["overall_price_range"];
    obj["rera_possession"] = projcts[index]["rera_possession"] ;
    obj["location"] = projcts[index]["location"];
    var configs = JSON.parse(projcts[index]["configs"]);
    if (configs != null) {
        for (let i = 0; i < configs.length; i++) {
            if (configs[i]["config"] == "2BHK") {
                const c = configs[i];
                obj["config" + i] = configs[i]["config"];
                obj["area" + i] = configs[i]["area"];
                obj["price" + i] = configs[i]["price"] / 100000;
                finalResult.push(obj);
            }
        }   
    }
}

console.log(finalResult);

csvWriter.writeRecords(finalResult)       // returns a promise
    .then(() => {
        console.log('...Done');
    });
