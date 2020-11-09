import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django_graphql_insights.insights.models import User, Group

# Create a GraphQL type for the user model
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Create a GraphQL type for the group model
class GroupType(DjangoObjectType):
    class Meta:
        model = Group

# Create a Query type
class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    group = graphene.Field(GroupType, id=graphene.Int())
    users = graphene.List(UserType)
    groups = graphene.List(GroupType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Group.objects.get(pk=id)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_groups(self, info, **kwargs):
        return Group.objects.all()
        
        
# Create Input Object Types
class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()

class GroupInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    users = graphene.List(UserInput)


# Create mutations for users
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_instance = User(username=input.username)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.username = input.username
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)

# Create mutations for groups
class CreateGroup(graphene.Mutation):
    class Arguments:
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        users = []
        for user_input in input.users:
          user = User.objects.get(pk=user_input.id)
          if user is None:
            return CreateGroup(ok=False, group=None)
          users.append(user)
        group_instance = Group(
          name=input.name
          )
        group_instance.save()
        group_instance.users.set(users)
        return CreateGroup(ok=ok, group=group_instance)


class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        group_instance = Group.objects.get(pk=id)
        if group_instance:
            ok = True
            users = []
            for user_input in input.users:
              user = User.objects.get(pk=user_input.id)
              if user is None:
                return UpdateGroup(ok=False, group=None)
              users.append(user)
            group_instance.name=input.name
            group_instance.save()
            group_instance.users.set(users)
            return UpdateGroup(ok=ok, group=group_instance)
        return UpdateGroup(ok=ok, group=None)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_group = CreateGroup.Field()
    update_group = UpdateGroup.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)