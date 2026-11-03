// define the construtor
// for linked list node
#include "LinkedListNode.h"

LinkedListNode::LinkedListNode(int key): key(key){}
LinkedListNode::LinkedListNode(int key, LinkedListNode* next): key(key), next(next){}
LinkedListNode::LinkedListNode(const LinkedListNode& node): key(node.key), next(node.next){}

