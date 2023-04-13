import { Modal } from "flowbite";
import type { ModalOptions, ModalInterface } from 'flowbite'

// /*
//  * $editUserModal: required
//  * options: optional
//  */

// // For your js code

const $modalElement: HTMLElement = document.querySelector('#editUserModal');


let userId: string = '';

const modalOptions: ModalOptions = {
    placement: 'bottom-right',
    backdrop: 'dynamic',
    backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
    closable: true,
    onHide: () => {
        console.log('modal is hidden');
    },
    onShow: () => {
        console.log('user id: ', userId);
    },
    onToggle: () => {
        console.log('modal has been toggled');
    }
}

const modal: ModalInterface = new Modal($modalElement, modalOptions);

const $buttonElements = document.querySelectorAll('.user-edit-button');
$buttonElements.forEach(e => e.addEventListener('click',()=>{editUser(e.getAttribute('data-target'))}))
const $buttonClose = document.querySelector('#modalCloseButton');
$buttonClose.addEventListener('click',()=>{modal.hide()})



function editUser(id: string) {
    userId = id;
    modal.show()

}
