

$('#add-more-specs').on("click",(e)=>{
    
    if (e) {
        e.preventDefault();
    }

    add_new_form("productspecification_set","specs-form","empty-form")
});

$('#add-more-images').on("click",(e)=>{
    
    if (e) {
        e.preventDefault();
    }

    add_new_form("images","images-form","empty-form2")
});

// function add_new_form(event) {

//     if (event) {
//         event.preventDefault()
//     }
//     // const currentFormCount = totalNewForms.value;
//     // const formCopyTarget = document.getElementById('specs-form')
//     // const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
//     // copyEmptyFormEl.setAttribute('class', 'specs-form-item')
//     // copyEmptyFormEl.setAttribute('id', `form-${currentFormCount}`)
//     // const regex = new RegExp('__prefix__', 'g')
//     // copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
//     // totalNewForms.setAttribute('value', Number(currentFormCount) + Number(1))
//     // formCopyTarget.append(copyEmptyFormEl)
// }

function add_new_form(prefix,formset_table,form_template) {


    var TotalFormsNumber = document.getElementById(`id_${prefix}-TOTAL_FORMS`)
    // index of new added form
    var currentFormCount = TotalFormsNumber.value;
    // empty template form copy
    var newForm = document.getElementById(form_template).cloneNode(true)
    // initializ new added form
    newForm.setAttribute('class', `${formset_table}-item`);
    newForm.setAttribute('id', `form-${currentFormCount}`)
    //replace _prefix_ with form index
    var regex = new RegExp('__prefix__', 'g')
    newForm.innerHTML = newForm.innerHTML.replace(regex, currentFormCount)
    TotalFormsNumber.setAttribute('value', Number(currentFormCount) + Number(1))
    // append new form
    document.getElementById(formset_table).tBodies[0].append(newForm);

}


