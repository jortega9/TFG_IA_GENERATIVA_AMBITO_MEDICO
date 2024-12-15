import { useState } from 'react';
import { PlusCircle } from 'lucide-react';
import { Button, Input } from '@mui/material';
import { Menu, MenuItem } from '@mui/material';
import '../styles/ChatList.css';

const ChatList = ({ chats, setChats, onSelectChat }) => {
    const [newChatName, setNewChatName] = useState('');
    const [menu, setMenu] = useState(null);

    const handleMenuOpen = (event) => {
        event.stopPropagation();
        setMenu(event.currentTarget);
    };

    const handleMenuClose = () => {
        setMenu(null);
    };

    const createNewChat = () => {
        if (newChatName.trim() === '') return;

        const newChat = {
            id: chats.length + 1,
            name: newChatName.trim(),
            messages: [],
        };
        
        setChats((prevChats) => [...prevChats, newChat]);
        setNewChatName('');
    };

    const changeChatName = () => {
        // Functionality for changing chat name
    };

    const deleteChat = (id) => {
        setMenu(null);
        setChats((prevChats) => prevChats.filter((chat) => chat.id !== id));
    };

    return (
        <div className="chat-list-container">
            <div className="flex gap-2 mb-4">
                <Input
                    type="text"
                    placeholder="Enter chat name"
                    value={newChatName}
                    onChange={(e) => setNewChatName(e.target.value)}
                    className="input-chatList"s
                />
                <Button
                    onClick={createNewChat}
                    disabled={newChatName.trim() === ''}
                    style={{ color: '#4D7AFF' }}
                >
                    <PlusCircle style={{ marginRight: '7px', color: '#4D7AFF' }} />
                    New Patient
                </Button>
            </div>

            <div className="chatName">
                {chats.map((chat) => (
                    <Button
                        key={chat.id}
                        className="chat-button"
                        onClick={() => onSelectChat(chat.id)}
                    >
                        {chat.name}
                        <span
                            onClick={handleMenuOpen}
                            style={{ fontSize: '15px', cursor: 'pointer' }}
                        >
                            ⋮
                        </span>
                        <Menu
                            anchorEl={menu}
                            open={Boolean(menu)}
                            onClose={handleMenuClose}
                        >
                            <MenuItem onClick={changeChatName}>Cambiar Nombre</MenuItem>
                            <MenuItem onClick={() => deleteChat(chat.id)}>Eliminar Paciente</MenuItem>
                        </Menu>
                    </Button>
                ))}
            </div>
        </div>
    );
};

export default ChatList;
