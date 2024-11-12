import React from "react";
import styles from "./delete-modal.module.css";
import Modal from "react-modal";

interface ComponentProps {
    warningMessage: string,
    deleteButtonName: string,
    cancelButtonName: string
    id: number|string,
    deleteFunction: (id: number|string) => void,
    onClose: () => void,
}

const DeleteModal: React.FC<ComponentProps> = ({ warningMessage, deleteButtonName, cancelButtonName, id, deleteFunction, onClose }) => {
    return (
        <Modal
            isOpen={true}
            onRequestClose={() => onClose()}
            overlayClassName={styles.deleteModalOverlay}
            className={styles.deleteModal}
            ariaHideApp={false}
        >
            <div className={styles.deleteModal}>
                <div className={styles.deleteModalClose}>
                    <a onClick={() => onClose()}>
                        X
                    </a>
                </div>
                <div className={styles.deleteModalMessage}>
                    {warningMessage}
                </div>
                <div className={styles.deleteModalButtonContainer}>
                    <button className={styles.deleteModalConfirm} onClick={() => deleteFunction(id)}>{deleteButtonName}</button>
                    <button className={styles.deleteModalCancel} onClick={() => onClose()}>{cancelButtonName}</button>
                </div>
            </div>    
        </Modal>
    );
}

export default DeleteModal;