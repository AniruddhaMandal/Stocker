window.onload = (event) => {
  let select_all_checkbox = document.getElementById("select_all_checkbox");
  let stock_checkbox = document.getElementsByClassName("stock_checkbox");
  select_all_checkbox.addEventListener("click",function () {
      for(let i = 0; i<stock_checkbox.length; i++){
          stock_checkbox[i].checked = true;
      }
  });
}
