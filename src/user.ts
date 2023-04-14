import { Modal } from "flowbite";
import type { ModalOptions, ModalInterface } from 'flowbite'

// /*
//  * $editUserModal: required
//  * options: optional
//  */

// // For your js code

interface IUser{
    id: number,
    username: string,
    email: string,
    activated: boolean,
}

const $modalElement: HTMLElement = document.querySelector('#editUserModal');


const modalOptions: ModalOptions = {
    placement: 'bottom-right',
    backdrop: 'dynamic',
    backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
    closable: true,
    onHide: () => {
        console.log('modal is hidden');
    },
    onShow: () => {
        console.log('user id: ');

        
    },
    onToggle: () => {
        console.log('modal has been toggled');
    }
}

const modal: ModalInterface = new Modal($modalElement, modalOptions);
 
export function initUsers() {

    const $buttonElements = document.querySelectorAll('.user-edit-button');
    $buttonElements.forEach(e => e.addEventListener('click', () => { editUser(JSON.parse(e.getAttribute('data-target'))) }))

    const $buttonClose = document.querySelector('#modalCloseButton');
    $buttonClose.addEventListener('click',()=>{modal.hide()})
}




function editUser(user: IUser) {
    // user-edit-username
    let input: HTMLInputElement = document.querySelector('#user-edit-username');
    input.value = user.username;
    input = document.querySelector('#user-edit-id');
    input.value = user.id.toString();
    input = document.querySelector('#user-edit-email');
    input.value = user.email;
    input = document.querySelector('#user-edit-password');
    input.value = "*******";
    input = document.querySelector('#user-edit-password_confirmation');
    input.value = "*******";
    input = document.querySelector('#user-edit-activated');
    input.checked = user.activated;

    modal.show();
}
