import { useState } from 'react';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Menu,
    MenuItem,
    TextField,
} from '@mui/material';
import { PlusCircle } from 'lucide-react';
import '../styles/ChatList.css';

const ChatList = ({ chats, setChats, onSelectChat }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newPatient, setNewPatient] = useState({ name: '', age: '', email: '' });
    const [menuAnchor, setMenuAnchor] = useState(null);
    const [selectedChatId, setSelectedChatId] = useState(null);

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setNewPatient({ name: '', age: '', email: '' });
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewPatient((prev) => ({ ...prev, [name]: value }));
    };

    const handleAddPatient = () => {
        if (!newPatient.name.trim()) return;

        const newChat = {
            id: chats.length + 1,
            name: newPatient.name.trim(),
            details: { age: newPatient.age, email: newPatient.email },
            messages: [],
        };

        setChats((prevChats) => [...prevChats, newChat]);
        handleCloseModal();
    };

    const handleMenuOpen = (event, chatId) => {
        setMenuAnchor(event.currentTarget);
        setSelectedChatId(chatId);
    };

    const handleMenuClose = () => {
        setMenuAnchor(null);
        setSelectedChatId(null);
    };

    const handleChangeChatName = () => {
        const newName = prompt('Ingrese el nuevo nombre del paciente:');
        if (newName && selectedChatId !== null) {
            setChats((prevChats) =>
                prevChats.map((chat) =>
                    chat.id === selectedChatId ? { ...chat, name: newName } : chat
                )
            );
        }
        handleMenuClose();
    };

    const handleDeleteChat = () => {
        if (selectedChatId !== null) {
            setChats((prevChats) => prevChats.filter((chat) => chat.id !== selectedChatId));
        }
        handleMenuClose();
    };

    return (
        <div className="chat-list-container">
            <div className="flex gap-2 mb-4">
                <Button onClick={handleOpenModal} style={{ color: '#4D7AFF' }}>
                    <PlusCircle style={{ marginRight: '7px', color: '#4D7AFF' }} />
                    Nuevo Paciente
                </Button>
            </div>

            {/* Mostramos la lista de pacientes */}
            <div className="chatName">
                {chats.map((chat) => (
                    <Button
                        key={chat.id}
                        className="chat-button"
                        onClick={() => onSelectChat(chat.id)}
                    >
                        {chat.name}
                        <span
                            onClick={(event) => handleMenuOpen(event, chat.id)}
                            style={{ fontSize: '15px', cursor: 'pointer', marginLeft: '10px' }}
                        >
                            ⋮
                        </span>
                        <Menu
                            anchorEl={menuAnchor}
                            open={Boolean(menuAnchor) && selectedChatId === chat.id}
                            onClose={handleMenuClose}
                        >
                            <MenuItem onClick={handleChangeChatName}>
                                Cambiar Nombre
                            </MenuItem>
                            <MenuItem onClick={handleDeleteChat}>
                                Dar de Baja Paciente
                            </MenuItem>
                        </Menu>
                    </Button>
                ))}
            </div>

            {/* Agregamos nuevo paciente mediante un formulario con la informacioón del paciente*/}
            <Dialog open={isModalOpen} onClose={handleCloseModal}>
                <DialogTitle>Agregar Nuevo Paciente</DialogTitle>
                <DialogContent>
                    <TextField
                        name="name"
                        label="Nombre"
                        value={newPatient.name}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="age"
                        label="Edad"
                        value={newPatient.age}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                        type="number"
                    />
                    <TextField
                        name="email"
                        label="Correo Electrónico"
                        value={newPatient.email}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                        type="email"
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseModal} color="secondary">
                        Cancelar
                    </Button>
                    <Button onClick={handleAddPatient} color="primary">
                        Agregar
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
};

export default ChatList;
