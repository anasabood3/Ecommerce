export function add_new_form(formset_table) {

    const TotalFormsNumber = document.getElementById('id_productspecification_set-TOTAL_FORMS')
    
    // index of new added form
    const currentFormCount = TotalFormsNumber.value;
    // empty template form copy
    const newForm = document.getElementById('empty-form').cloneNode(true)
    // initializ new added form
    newForm.setAttribute('class', `${container_name}-item`);
    newForm.setAttribute('id', `form-${currentFormCount}`)
    //replace _prefix_ with form index
    const regex = new RegExp('__prefix__', 'g')
    newForm.innerHTML = newForm.innerHTML.replace(regex, currentFormCount)
    TotalFormsNumber.setAttribute('value', Number(currentFormCount) + Number(1))
    // append new form
    const formsetContainer = document.getElementById(formset_table);
    formsetContainer.tBodies[0].prepend(newForm);
    scsscasc= scjsc;

}