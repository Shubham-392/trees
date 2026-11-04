#include "UnSyncLinkedList.h"
#include <vector>
#include <iostream>


UnSyncLinkedList::UnSyncLinkedList(const std::vector<int>& arr){
    // we have to insert the element from arr
    for (const auto& key: arr){
        m_add(key);
    }
}


void UnSyncLinkedList::m_add(int key){
    LinkedListNode* new_node = new LinkedListNode(key);
    if (m_head == nullptr){
        m_head = new_node;
        m_tail = new_node;
    } else {
        m_tail->next = new_node;
        m_tail = new_node;
    }
    // increase the size gloally
    m_size++;
}


bool UnSyncLinkedList::m_remove(int key){
    if (m_size == 0){
        return false;
    }

    else if(m_size == 1){
        if(m_head->key == key){
            delete m_head;
            m_head = nullptr;
            m_tail = nullptr;
            m_size = 0;
            return true;
        }
        return false;
    }

    else{
        if (m_head->key == key){
            LinkedListNode* temp = m_head;
            m_head = m_head->next;
            delete temp;
            m_size--;
            return true;
        }

        LinkedListNode* prev = m_head;
        LinkedListNode* curr = m_head->next;

        while(curr != nullptr){
            if(curr->key == key){
                prev->next = curr->next;
                if (curr == m_tail){
                    m_tail = prev;
                }
                delete curr;
                m_size--;
                return true;
            }
            prev = curr;
            curr = curr->next;
        }

        return false;
    }
}
int UnSyncLinkedList::m_getSize(){
    return m_size;
}


void UnSyncLinkedList::m_display(){
    if (m_head == nullptr){
        std::cout << "list is empty" << std::endl;
        return;
    }

    LinkedListNode* curr = m_head;
    while (curr != nullptr){
        std::cout << curr->key;
        if (curr->next != nullptr){
            std::cout << " -> ";
        }
        curr = curr->next;
    }
    std::cout << std::endl;
}