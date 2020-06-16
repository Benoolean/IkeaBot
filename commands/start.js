module.exports.run = async (bot, message, args) => {
    let fs = require("fs");
    let file = fs.readFileSync("data/ikea_products.txt", "utf8");

    let category_arr = [];
    file.forEach((line, idx) => {
        if(line.includes("URL")) {
            let category = (idx + 1) + "|" + line.substring(4);
            category_arr.push(category);
        }
    });

    // getting the category
    let category_index = randomInt(0, category_arr.length);
    let category = category_arr[category_index];
    let next_category = (category_index < category_arr.length - 1) ? category_arr[category_index + 1] : null;

    // getting the product
    // regex for getting all char before the : char
    let min_index = category.match(/^[^|]+/);

    // Since there is a space between each category, we remove 2 from the max_index
    let max_index = (next_category != null) ? next_category.match(/^[^|]+/) - 2 : -1;  

    // resulting product
    let result_index = randomInt(parseInt(min_index) + 1, (max_index != -1 ? parseInt(max_index) : file.length - 2));

    // iterating the file until the result_index. Worst case runtime O(n)
    file.forEach((line, index) => {
        if (result_index == index) {
            console.log(line);
            
            // scraping ikea product by URL
            let {PythonShell} = require('python-shell');
            let options = {
                mode: 'text',
                args: [line]
            };

            PythonShell.run('core_scrape/ikea_product_scraper/product_spider.py', options, function (err) {
                if (err) 
                    throw err;
                
                console.log('Scraping completed');
                // format message
                message_output = ':fork_and_knife: A new IKEA product has arrived! Claim it before it is gone! :fork_and_knife:\nCategory: '

                let data_file = fs.readFile("core_scrape/ikea_product_scraper/crawled/product_data.json", function(err, data) {
                    if (err) 
                        throw err; 
                    
                    // Converting to JSON 
                    const product_data = JSON.parse(data);
                });

                message_output = message_output + category.match(/[^|]*$/);

                message.channel.send(message_output, {files: ['core_scrape/ikea_product_scraper/crawled/product_image.jpg']});
            });
        }   
    });
    
}

module.exports.description = {
    name: 'start'
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}