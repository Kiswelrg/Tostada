import { createApp } from 'vue'

const clickOutside = {
  updated: (el, binding, vnode) => {
    const args = binding.value; // Assuming binding.value is an array
    const triggeringElement = args?.length > 1 ? args[1] : null;
    const callback = args ? args[0] : null; // Assuming the first argument is the callback function
  
    el.clickOutsideEvent = (event) => {
      
      if (
        !(el === event.target || el.contains(event.target)) &&
        (!triggeringElement || ( // if no triggering button, then AND true
          !triggeringElement.contains(event.target) && event.target !== triggeringElement
        ))
      ) {
        if (callback != null){
          console.log('called the callback function');
          // console.log(event.target);
          // console.log(el);
          callback(); // Call the callback function
        }
      } else {
        console.log('inside')
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted: (el) => {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}

export default clickOutside