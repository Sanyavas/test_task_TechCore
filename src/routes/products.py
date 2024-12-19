from schemas.products import ProductResponse

router = APIRouter(tags=["Contacts"], prefix='/contacts')


@router.get(path="/",
            response_model=list[ProductResponse],
            summary="Get all contacts")
async def get_contacts(db: AsyncSession = Depends(get_db)):
    """Отримати всі контакти."""
    contacts = await repo_contacts.get_contacts(db)
    return contacts


@router.get(path="/{contact_id}",
            response_model=ProductResponse,
            summary="Get contact by ID")
async def get_contact(contact_id: UUID, db: AsyncSession = Depends(get_db)):
    """Отримати контакт за унікальним ID."""
    contact = await repo_contacts.get_contact_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ContactMessages.NOT_FOUND)
    return contact


@router.post(path="/",
             response_model=ProductResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new contact")
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    """Створити новий контакт."""
    existing_contact = await repo_contacts.get_contact_by_email(str(body.email), db) #TODO
    if existing_contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ContactMessages.EMAIL_ALREADY_EXISTS)
    contact = await repo_contacts.create_contact(body, db)
    return contact


@router.put(path="/{contact_id}",
            response_model=ContactResponse,
            summary="Update contact by ID")
async def update_contact(body: ContactModel, contact_id: UUID, db: AsyncSession = Depends(get_db)):
    """Оновити контакт за його унікальним ID."""
    contact = await repo_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ContactMessages.NOT_FOUND)
    return contact


@router.delete(path="/{contact_id}",
               response_model=dict,
               summary="Delete contact by ID")
async def delete_contact(contact_id: UUID, db: AsyncSession = Depends(get_db)):
    """Видалити контакт за його унікальним ID."""
    contact = await repo_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ContactMessages.NOT_FOUND)
    return {"detail": ContactMessages.DELETED_CONTACT}