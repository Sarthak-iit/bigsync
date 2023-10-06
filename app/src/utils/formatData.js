const formatData = async(data) => {
    let columns = Object.keys(data[0]);
    columns = columns.slice(1,)
    const data_column = {};
    for (const row of data) {
        for (const columnName in row) {
            if (!data_column[columnName]) {
                data_column[columnName] = [];
            }
            data_column[columnName].push(row[columnName]);
        }
    }
    const time = data_column['Time'];
    console.log('time',time);
    const char = ['F', 'VM', 'VA', 'IM', 'IA']
    const d = ['', '_1', '_2', '_3', '_4']
    let sub = []
    
    columns.forEach((val, i) => {
        if (i % 5 === 0) { sub.push(val) }
    })
    let formatted_data = {}
    sub.forEach((val) => {
        let temp = {}
        for (let j = 0; j < 5; j++) {
            temp[char[j]] = data_column[`${val}` + d[j]]
        }
        formatted_data[val] = temp;
    })
    return [time,formatted_data]
}
export default formatData