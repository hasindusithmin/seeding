
const entry = () => {
    sessionStorage.clear()
    const table_name = document.createElement('input');
    table_name.id = 'question_1';
    table_name.placeholder = 'Enter table name';
    table_name.onchange = e => {
        const _ = e.target.value;
        sessionStorage.setItem('table_name',_)
        ask_question_2()
    }
    document.getElementById('root').appendChild(table_name)
}

const ask_question_2 = () => {
    document.getElementById('root').innerText = ''
    const fieldqty = document.createElement('input');
    fieldqty.placeholder = 'Field Quantity'
    fieldqty.id = 'question_2';
    fieldqty.placeholder = 'Enter number of fields';
    fieldqty.type = 'number'
    fieldqty.onchange = e => {
        const _ = e.target.value;
        sessionStorage.setItem('fieldqty',_)
        ask_question_3(_)
    }
    document.getElementById('root').appendChild(fieldqty)
}

const ask_question_3 = async () => {
    document.getElementById('root').innerText = ''
    const fieldqty = sessionStorage.getItem('fieldqty')
    const res = await fetch('/available')
    const data = await res.json()
    for (let i = 1; i <= parseInt(fieldqty); i++) {
        document.getElementById('root').appendChild(genOptions(data, i))
    }
    const btn = document.createElement('button');
    btn.innerText = 'Ok';
    btn.onclick = ()=>{
        const qty = sessionStorage.getItem('fieldqty');
        const fields = []
        for (let i = 1;i <= parseInt(qty);i++) {
            const value = sessionStorage.getItem(`Field${i}`)
            if (fields.includes(value)) {
                alert('detect duplication')
                window.location.reload()
                break
            }
            fields.push(value)
        }
        if (fields.includes(null)) {
            alert('detect null field')
            window.location.reload()
        }
        sessionStorage.setItem('fields',JSON.stringify([...new Set(fields)]))
        ask_question_4()
    }
    document.getElementById('root').appendChild(btn);
}

const genOptions = (data, index) => {
    const div = document.createElement('div');
    const h5 = document.createElement('h5');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox'
    const span = document.createElement('span')
    span.innerHTML = 'Not Null'
    h5.innerText = `Field ${index}`;
    const select = document.createElement('select');
    const option = document.createElement('option');
    option.innerText = "select"
    select.appendChild(option)
    for (const { method, desc } of data) {
        const option = document.createElement('option');
        option.value = method;
        option.innerText = method;
        option.title = desc
        select.appendChild(option);
    }
    select.onchange = e => {
        h5.innerText = e.target.value;
        sessionStorage.setItem(`Field${index}`,e.target.value)
    }
    sessionStorage.setItem('notnull',JSON.stringify([]))
    checkbox.onclick = e => {
        let notnull = JSON.parse(sessionStorage.getItem('notnull'))
        notnull.push(index)
        sessionStorage.setItem('notnull',JSON.stringify(notnull))
    }
    div.appendChild(h5);
    div.appendChild(select);
    div.appendChild(span);
    div.appendChild(checkbox);
    return div;
}

const ask_question_4 = ()=>{
    document.getElementById('root').innerText = ''
    const rowqty = document.createElement('input');
    rowqty.placeholder = 'Row Quantity'
    rowqty.placeholder = 'Enter number of rows';
    rowqty.type = 'number'
    rowqty.onchange = e => {
        const _ = e.target.value;
        sessionStorage.setItem('rowqty',_)
        genFile()
    }
    document.getElementById('root').appendChild(rowqty)
}

const genFile = ()=>{
    let url = '/gen?'
    const fields = JSON.parse(sessionStorage.getItem('fields'))
    const notnull = JSON.parse(sessionStorage.getItem('notnull'))
    const rowqty = sessionStorage.getItem('rowqty')
    const table = sessionStorage.getItem('table_name')
    fields.forEach(field => {
        url += `field=${field}&`
    });
    notnull.forEach(elem => {
        url += `notnull=${elem}&`
    });
    url += `rowqty=${rowqty}&`
    url += `table=${table}`
    console.log(url);
    fetch(url,{
        method:'GET',
        headers:{
            'Content-Type': 'application/json'
        }
    })
        .then((res)=>res.json())
        .then(data=>{
            console.log(data);
        })
}

entry()