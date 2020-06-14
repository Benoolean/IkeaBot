
module.exports = {
    name: 'ikea',
    description: 'Gets random product and initialize capture',
    execute(msg) {
        if (msg.author.id === "318439813206376448" || true) {
            msg.channel.send("Debugging Authenticated for: " + msg.author.username + "#" + msg.author.discriminator);

            var fs = require("fs");
            let file = fs.readFileSync("data/ikea_products.txt", "utf8").split(/\r?\n/);

            category_arr = [];
            file.forEach((line, idx) => {
                if(line.includes("URL")) {
                    category = (idx + 1) + "|" + line.substring(4);
                    category_arr.push(category);
                }
            });

            // getting the category
            var category_index = randomInt(0, category_arr.length);
            var category = category_arr[category_index];
            var next_category = (category_index < category_arr.length - 1) ? category_arr[category_index + 1] : null;

            // getting the product
            // regex for getting all char before the : char
            var min_index = category.match(/^[^|]+/);

            // Since there is a space between each category, we remove 2 from the max_index
            var max_index = (next_category != null) ? next_category.match(/^[^|]+/) - 2 : -1;  

            // resulting product
            var result_index = randomInt(parseInt(min_index) + 1, (max_index != -1 ? parseInt(max_index) : file.length - 2));
            
            // console.log('======');
            // console.log('DEBUG:');
            // console.log('Cat: ' + category + ' CatIdx: ' + category_index + ' CatLen: ' + category_arr.length);
            // console.log('Min: ' + min_index + ' Max: ' + max_index);
            // console.log('Result: ' + result_index);
            // console.log('======');

            // iterating the file until the result_index. Worst case runtime O(n)
            file.forEach((line, index) => {
                if (result_index == index) {
                    console.log(line);
                    
                    // scraping ikea product by URL
                    let {PythonShell} = require('python-shell')
                    var options = {
                        mode: 'text',
                        args: [line]
                    }
                    
                    PythonShell.run('core_scrape/ikea_product_scraper/product_spider.py', options, function (err) {
                        if (err) 
                            throw err;

                        console.log('Scraping complete');
                    });
                    
                    // send message
                    msg.channel.send(category.match(/[^|]*$/) + " | " + line);
                    return;
                }   
            });
        }
        
    }
}


function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}