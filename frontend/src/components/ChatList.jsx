import { useState, useEffect } from 'react';
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

/**
 * 
 * Lista de chats de pacientes
 * Funcionalidad no empleada en la aplicación
 * 
 * @param {*} param0 
 * @returns 
 */
const ChatList = ({ chats, setChats, onSelectChat }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newPatient, setNewPatient] = useState({
        name: '',
        email: '',
        age: '',
        phone: '',
        gender: '',
        diseases: '',
        allergy: '',
    });
    const [menuAnchor, setMenuAnchor] = useState(null);
    const [selectedChatId, setSelectedChatId] = useState(null);
    const [isUpdating, setIsUpdating] = useState(false)
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/auth/patients', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
    
                if (!response.ok) {
                    throw new Error('Error al obtener los pacientes');
                }
    
                const patients = await response.json();
                setChats(patients);
                console.log('Pacientes obtenidos: ', patients);
            } catch (error) {
                console.error('Error al obtener los pacientes:', error);
            }
        };
    
        fetchPatients();
    }, [refresh]);

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setNewPatient({
            name: '',
            email: '',
            age: '',
            phone: '',
            gender: '',
            diseases: '',
            allergy: '',
        });
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewPatient((prev) => ({ ...prev, [name]: value }));
    };

    const handleAddPatient = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/newPatient', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newPatient),
            });

            if (!response.ok) {
                throw new Error('Error al añadir el paciente');
            }

            const result = await response.json();
            console.log('Paciente añadido:', result);
            setRefresh((prev) => !prev);

            handleCloseModal();
        } catch (error) {
            console.error('Error al añadir el paciente:', error);
        }
    };

    const handleMenuOpen = (event, chatId) => {
        setMenuAnchor(event.currentTarget);
        setSelectedChatId(chatId);
    };

    const handleMenuClose = () => {
        setMenuAnchor(null);
        setSelectedChatId(null);
        setIsUpdating(false);
    };

    const handleMenuOpenUpdate = () => {
        setIsUpdating(true);
        setIsModalOpen(true);
    };

    const handleDeletePatient = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/auth/delete/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Error al eliminar el paciente');
            }

            const result = await response.json();
            console.log('Paciente eliminado:', result);
            setRefresh((prev) => !prev);

            handleCloseModal();
        } catch (error) {
            console.error('Error al eliminar el paciente:', error);
        }
    };

    return (
        <div className="chat-list-container">
            <div className="flex gap-2 mb-4">
                <Button onClick={handleOpenModal} style={{ color: '#4D7AFF' }}>
                    <PlusCircle style={{ marginRight: '7px', color: '#4D7AFF' }} />
                    Nuevo Paciente
                </Button>
            </div>

            <div className="chatName">
                {chats.map((chat) => (
                    <Button
                        key={chat.id}
                        className="chat-button"
                        onClick={() => onSelectChat(chat[0])}
                    >
                        {chat[1]?.split(' ').slice(0, 2).join(' ')}
                        <span
                            onClick={(event) => handleMenuOpen(event, chat[0])}
                            style={{ fontSize: '15px', cursor: 'pointer', marginLeft: '10px' }}
                        >
                            ⋮
                        </span>
                        <Menu
                            anchorEl={menuAnchor}
                            open={Boolean(menuAnchor) && selectedChatId === chat[0]}
                            onClose={handleMenuClose}
                        >
                            <MenuItem onClick={handleMenuOpenUpdate}>
                                Cambiar Información Paciente
                            </MenuItem>
                            <MenuItem onClick={() => handleDeletePatient(chat[0])}>
                                Dar de Baja Paciente
                            </MenuItem>
                        </Menu>
                    </Button>
                ))}
            </div>

            <Dialog open={isModalOpen} onClose={handleCloseModal}>
                <DialogTitle>
                    {isUpdating ? 'Actualizar Información del Paciente' : 'Agregar Nuevo Paciente'}
                </DialogTitle>
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
                    <TextField
                        name="phone"
                        label="Teléfono"
                        value={newPatient.phone}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="gender"
                        label="Género"
                        value={newPatient.gender}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="diseases"
                        label="Enfermedades"
                        value={newPatient.diseases}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                    />
                    <TextField
                        name="allergy"
                        label="Alergias"
                        value={newPatient.allergy}
                        onChange={handleInputChange}
                        fullWidth
                        margin="normal"
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseModal} color="secondary">
                        Cancelar
                    </Button>
                    <Button onClick={handleAddPatient} color="primary">
                        {isUpdating ? 'Actualizar' : 'Agregar'}
                    </Button>
                </DialogActions>
            </Dialog>

        </div>
    );
};

export default ChatList;
